# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""
LocalSGD
=========
This module implements a fault tolerant version of LocalSGD and related methods.
"""
import logging
from types import TracebackType
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Type

import torch
from torch import nn, optim
from torch.distributed.tensor import DTensor
from torch.nn.parameter import Parameter
from torch.optim.optimizer import Optimizer
from torch.utils.hooks import RemovableHandle

from torchft.manager import Manager

logger: logging.Logger = logging.getLogger(__name__)


def extract_local_tensor(t: torch.Tensor) -> torch.Tensor:
    """
    Returns a cloned version of the input tensor. If the input tensor is a DTensor,
    it extracts and clones its local representation.
    """
    new_tensor = None
    if isinstance(t, DTensor):
        new_tensor = t.to_local().clone()
    else:
        new_tensor = t.clone()
    new_tensor.grad = None
    return new_tensor


class LocalSGD:
    """
    LocalSGD is a context manager that
    implements the algorithm described in https://arxiv.org/pdf/1805.09767

    This will synchronize the model parameters periodically in a fault tolerant
    way using a torchft Manager. The allreduce on the parameters will happen
    every sync_every steps after the optimizer.step call.

    The torchft quorum is computed at the beginning of ``sync_every`` steps. If
    any error occurs, or a worker fails between syncs, ``sync_every`` steps will be
    discarded and a new quorum will be computed on the next step.

    If running in async mode, on a joining worker the first ``sync_every`` steps
    will discarded as the model will be recovering during that period. When
    using sync mode, the checkpoint will be restored prior to the first step.
    """

    def __init__(
        self,
        manager: Manager,
        model: nn.Module,
        optimizer: optim.Optimizer,
        sync_every: int,
    ) -> None:
        """
        Args:
            manager: The manager to use.
            model: The model to wrap.
            optimizer: The optimizer used by the model.
            sync_every: How often to sync the model weights.
        """
        super().__init__()
        self._manager = manager
        self._model = model
        self._local_optimizer = optimizer
        self._local_step = 0
        self._sync_every = sync_every
        assert sync_every >= 1, "sync_every must be greater than or equal to 1"

        self._hooks: List[RemovableHandle] = []

    def __enter__(self) -> "LocalSGD":
        # Add optimizer hook which increments the local step counter and syncs if necessary
        self._hooks.append(
            self._local_optimizer.register_step_post_hook(self._step_post_hook)
        )
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        # Handle any cleanup or error handling here
        # Clean up hooks
        for hook in self._hooks:
            hook.remove()
        self._hooks.clear()

        return False  # Propagate exceptions

    def _step_post_hook(
        self, _optim: optim.Optimizer, _args: Tuple[Any, ...], _kwargs: Dict[str, Any]
    ) -> None:
        """
        This hook is registered on the optimizer and is called after the optimizer step.
        """
        self._local_step += 1
        if self._local_step >= self._sync_every:
            self.sync()

    def sync(self) -> None:
        """
        Synchronizes and averages the model weights across the manager.
        """
        self._manager.start_quorum()
        self._perform_sync()
        self._local_step = 0

    def _perform_sync(self) -> None:
        """
        Performs the synchronization of the model weights across the manager.
        """
        averaged_parameters = self._average()
        if self._manager.should_commit():
            # Update the model parameters with the averaged values
            for param, avg_param in zip(self._model.parameters(), averaged_parameters):
                if isinstance(param, DTensor):
                    # we averaged the local version of the tensor so need to copy it back as a DTensor
                    param.data.copy_(
                        DTensor.from_local(
                            avg_param, param.device_mesh, param.placements
                        )
                    )
                else:
                    param.data.copy_(avg_param)

    def _average(self) -> list[torch.Tensor]:
        """
        Averages the model parameters across the manager and returns the averaged parameters.
        """
        works = []
        averaged_parameters = []
        for p in self._model.parameters():
            # Create a new tensor to store the averaged parameter
            avg_param = extract_local_tensor(p)
            works.append(self._manager.allreduce(avg_param))
            averaged_parameters.append(avg_param)
        for work in works:
            work.wait()
        return averaged_parameters


class DiLoCo:
    """
    DiLoCo is a subclass of LocalSGD that overrides the synchronization
    mechanism to average and synchronize the pseudogradients (delta of the previous global weight and current local weights).

    This algorithm requires a backup copy of the
    weights. By default these are stored in CPU memory. If any error occurs
    during the DiLoCo step, the step will be discarded and the model
    parameters will reset back to the last time DiLoCo synchronized.

    DiLoCo paper: https://arxiv.org/pdf/2311.08105
    """

    def __init__(
        self,
        manager: Manager,
        model: nn.Module,
        inner_optimizer: optim.Optimizer,
        outer_optimizer: optim.Optimizer,
        sync_every: int,
        backup_device: Optional[torch.device] = None,
        pin_memory: bool = True,
    ) -> None:
        """
        Args:
            manager: The manager to use.
            model: The model to wrap.
            inner_optimizer: The optimizer used for the local parameters every step.
            outer_optimizer: The optimizer used for the global parameters updated every "sync_every" steps.
            sync_every: How often to update the model weights.
            backup_device: The device to store the backup weights on. If None, the backup weights will be on CPU.
            pin_memory: Whether to pin the memory for the backup weights (only for CPU device).
        """

        if manager._use_async_quorum:
            raise ValueError(
                "Using DiLoCo require synchronous quorum to be enabled. "
                "Ensure that the manager is initialized with use_async_quorum=False"
            )
        super().__init__()
        self._manager = manager
        self._model = model
        self._local_optimizer = inner_optimizer
        self._local_step = 0
        self._sync_every = sync_every
        assert sync_every >= 1, "sync_every must be greater than or equal to 1"
        self._backup_device = backup_device
        self._pin_memory = pin_memory

        self._hooks: List[RemovableHandle] = []
        self._outer_optimizer = outer_optimizer
        self.original_parameters: Dict[str, torch.Tensor] = {}
        for name, p in self._model.named_parameters():
            if isinstance(p, DTensor):
                p = extract_local_tensor(p.data)

            backup_device = self._backup_device or torch.device("cpu")
            t = torch.empty(*tuple(p.shape), dtype=p.dtype, device=backup_device)
            if (
                self._pin_memory
                and t.device == torch.device("cpu")
                and torch.cuda.is_available()
            ):
                t = t.pin_memory()
            self.original_parameters[name] = t

        # Need to copy the parameters to the host to be safe if we are on the first step.
        self._save_parameters()

    def _save_parameters(self) -> None:
        with torch.no_grad():
            # TODO: consider running copy on a separate stream
            for name, p in self._model.named_parameters():
                param_to_local = extract_local_tensor(p.data)
                self.original_parameters[name].copy_(param_to_local, non_blocking=True)

    def _restore_parameters(self) -> None:
        with torch.no_grad():
            # TODO: consider running copy on a separate stream
            for name, p in self._model.named_parameters():
                if isinstance(p, DTensor):
                    # we averaged the local version of the tensor so need to copy it back as a DTensor
                    p.data.copy_(
                        DTensor.from_local(
                            self.original_parameters[name], p.device_mesh, p.placements
                        ),
                        non_blocking=False,
                    )
                else:
                    p.data.copy_(self.original_parameters[name], non_blocking=False)

    def __enter__(self) -> "DiLoCo":
        # Add optimizer hook which increments the local step counter and syncs if necessary
        self._hooks.append(
            self._local_optimizer.register_step_post_hook(self._step_post_hook)
        )
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        # Handle any cleanup or error handling here
        # Clean up hooks
        for hook in self._hooks:
            hook.remove()
        self._hooks.clear()

        return False  # Propagate exceptions

    def _step_post_hook(
        self, _optim: optim.Optimizer, _args: Tuple[Any, ...], _kwargs: Dict[str, Any]
    ) -> None:
        """
        This hook is registered on the optimizer and is called after the optimizer step.
        """
        self._local_step += 1
        if self._local_step >= self._sync_every:
            self.sync()

    def sync(self) -> None:
        """
        Synchronizes and averages the model weights across the manager.
        """
        self._manager.start_quorum()
        self._perform_sync()
        self._local_step = 0

    def _perform_sync(self) -> None:
        """
        Overrides the sync method to calculate the pseugradient, average them across the manager group, and
        step using the outer optimizer.
        """
        # Set the .grad field of each parameter to its pseudogradient
        for name, p in self._model.named_parameters():
            local_param = extract_local_tensor(p.data)
            pseudogradient = local_param - self.original_parameters[name].to(p.device)
            if isinstance(p, DTensor):
                p.grad._local_tensor = pseudogradient
            else:
                p.grad = pseudogradient

        self._average_grads()
        # Restore the parameters back to the previous state
        self._restore_parameters()
        if self._manager.should_commit():
            # Use the outer optimizer to update the model parameters
            self._outer_optimizer.step()
            self._save_parameters()
        self._outer_optimizer.zero_grad()

    def _average_grads(self) -> None:
        """
        Average the gradients across the diloco group.
        """
        works = []
        for p in self._model.parameters():
            # Perform allreduce on the pseudogradients
            assert p.grad is not None
            if isinstance(p, DTensor):
                work = self._manager.allreduce(p.grad._local_tensor)
            else:
                work = self._manager.allreduce(p.grad)
            works.append(work)
        # Wait for all allreduce operations to complete
        for work in works:
            work.wait()
