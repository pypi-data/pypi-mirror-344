from __future__ import annotations
import warnings
from typing import List, Optional

import torch
from torch.nn.modules.loss import _Loss
import numpy as np
from gudhi import (
    wasserstein,
)

# TODO adjust that this package is in a plcace where betti matching and hutopo can accesss it
# from ...betti_matching.src import betti_matching
import sys, os

# sys.path.append(
#     "/home/computacenter/Documents/janek/topolosses/topolosses/losses/betti_matching/src/ext/Betti-Matching-3D-standalone-barcode/build"
# )
# from ...betti_matching.src import betti_matching  # C++ Implementation
# import betti_matching

# will this path also be available during build or should i do a relative path there?
from topolosses.losses.betti_matching.src import betti_matching

from ...utils import compute_default_dice_loss
from ...utils import FiltrationType


class HutopoLoss(_Loss):
    """Topology-preserving segmentation loss combining pixel-wise and topological objectives.

    This loss has been defined in:
        Hu et al. (2019) "Topology-Preserving Deep Image Segmentation" (NeurIPS),

    This loss penalizes discrepancies between persistence diagrams of predicted and ground-truth segmentations using a Wasserstein distance on birth–death pairs.
    This loss can be used standalone or combined with a base segmentation loss via a weighting factor \u03b1.
    """

    def __init__(
        self,
        filtration_type: FiltrationType | str = FiltrationType.SUPERLEVEL,
        num_processes: int = 1,
        include_background: bool = False,
        alpha: float = 0.5,
        softmax: bool = False,
        sigmoid: bool = False,
        use_base_loss: bool = True,
        base_loss: Optional[_Loss] = None,
    ) -> None:
        """
        Args:
            filtration_type (FiltrationType or string):
                Choose how to build the topological filtration on probability maps:
                  - `sublevel`:    sublevel-set on raw output.
                  - `superlevel`:  sublevel-set on inverted output (1–p).
                  - `bothlevels`:  both SUBLEVEL and SUPERLEVEL via concatenation.

                Defaults to SUPERLEVEL.
            num_processes (int):
                Number of parallel processes for persistent homology computations. Higher values may improve throughput. Defaults to 1.
            include_background (bool):
                Whether to include the background channel when computing topological loss. If False, only foreground classes are used. Defaults to False.
            alpha (float):
                Weight between the base segmentation loss and the topological loss. Total loss = base_loss + alpha * topo_loss. Defaults to 0.5.
            softmax (bool):
                If True, applies softmax to network outputs before loss computation. Mutually exclusive with sigmoid. Defaults to False.
            sigmoid (bool):
                If True, applies sigmoid activation to network outputs before loss computation. Mutually exclusive with softmax. Defaults to False.
            use_base_loss (bool):
                Whether to include a pixel-wise base loss component. If False, only the topological term is used and alpha is ignored. Defaults to True.
            base_loss (Optional[_Loss]):
                Custom base loss function (e.g., DiceLoss, CrossEntropy). If None and use_base_loss=True, a default Dice loss is used. Defaults to None.

        Raises:
            ValueError: If both sigmoid and softmax are set to True simultaneously.
            ValueError: If `filtration_type` is provided as a string but does not match any of the valid options ('SUPERLEVEL', 'SUBLEVEL', 'BOTHLEVELS').
        """
        if sum([sigmoid, softmax]) > 1:
            raise ValueError(
                "At most one of [sigmoid, softmax] can be set to True. "
                "You can only choose one of these options at a time or none if you already pass probabilites."
            )

        super(HutopoLoss, self).__init__()

        self.filtration_type = (
            FiltrationType(filtration_type) if not isinstance(filtration_type, FiltrationType) else filtration_type
        )
        self.filtration_type = filtration_type
        self.num_processes = num_processes
        self.include_background = include_background
        self.alpha = alpha
        self.softmax = softmax
        self.sigmoid = sigmoid
        self.use_base_loss = use_base_loss
        self.base_loss = base_loss

        if not self.use_base_loss:
            if base_loss is not None:
                warnings.warn("base_loss is ignored beacuse use_base_component is set to false")
            if self.alpha != 1:
                warnings.warn("Alpha < 1 has no effect when no base component is used.")

    def forward(self, input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Calculates the forward pass of the HutopoLoss.

        Args:
            input (Tensor): Input tensor of shape (batch_size, num_classes, H, W).
            target (Tensor): Target tensor of shape (batch_size, num_classes, H, W).

        Returns:
            Tensor: The calculated betti matching loss.

        Raises:
            ValueError: If the shape of the ground truth is different from the input shape.
            ValueError: If softmax=True and the number of channels for the prediction is 1.

        """
        if target.shape != input.shape:
            raise ValueError(f"ground truth has different shape ({target.shape}) from input ({input.shape})")

        starting_class = 0 if self.include_background else 1
        num_classes = input.shape[1]

        if num_classes == 1:
            if self.softmax:
                raise ValueError(
                    "softmax=True requires multiple channels for class probabilities, but received a single-channel input."
                )
            if not self.include_background:
                warnings.warn(
                    "Single-channel prediction detected. The `include_background=False` setting  will be ignored."
                )
                starting_class = 0

        # Avoiding applying transformations like sigmoid, softmax, or one-vs-rest before passing the input to the base loss function
        # These settings have to be controlled by the user when initializing the base loss function
        base_loss = torch.tensor(0.0)
        if self.alpha < 1 and self.use_base_loss and self.base_loss is not None:
            base_loss = self.base_loss(input, target)

        if self.sigmoid:
            input = torch.sigmoid(input)
        elif self.softmax:
            input = torch.softmax(input, 1)

        if self.alpha < 1 and self.use_base_loss and self.base_loss is None:
            base_loss = compute_default_dice_loss(input, target)

        hutopo_loss = torch.tensor(0.0)
        if self.alpha > 0:
            hutopo_loss = self.compute_hutopo_loss(
                input[:, starting_class:].float(),
                target[:, starting_class:].float(),
            )

        total_loss = hutopo_loss if not self.use_base_loss else base_loss + self.alpha * hutopo_loss

        return total_loss

    def compute_hutopo_loss(
        self,
        prediction: torch.Tensor,
        target: torch.Tensor,
    ) -> List[torch.Tensor]:
        """Compute the hutopo loss as the topological discrepancy by matching prediction and target persistence
        diagrams via a squared-L2 Wasserstein distance on birth–death pairs."""

        # Flatten out channel dimension to treat each channel as a separate instance for multiclass prediction
        # TODO this line is used in hutopo and betti matching so far, might be smart to move it either outside of these functions or to a parent class
        prediction = torch.flatten(prediction, start_dim=0, end_dim=1).unsqueeze(1)
        target = torch.flatten(target, start_dim=0, end_dim=1).unsqueeze(1)

        if self.filtration_type == FiltrationType.SUPERLEVEL:
            # Using (1 - ...) to allow binary sorting optimization on the label, which expects values [0, 1]
            prediction = 1 - prediction
            target = 1 - target
        if self.filtration_type == FiltrationType.BOTHLEVELS:
            # Just duplicate the number of elements in the batch, once with sublevel, once with superlevel
            prediction = torch.concat([prediction, 1 - prediction])
            target = torch.concat([target, 1 - target])

        split_indices = np.arange(self.num_processes, prediction.shape[0], self.num_processes)
        predictions_list_numpy = np.split(prediction.detach().cpu().numpy().astype(np.float64), split_indices)
        targets_list_numpy = np.split(target.detach().cpu().numpy().astype(np.float64), split_indices)

        losses = []

        current_instance_index = 0
        for predictions_cpu_batch, targets_cpu_batch in zip(predictions_list_numpy, targets_list_numpy):
            predictions_cpu_batch, targets_cpu_batch = list(predictions_cpu_batch.squeeze(1)), list(
                targets_cpu_batch.squeeze(1)
            )
            if not (
                all(a.data.contiguous for a in predictions_cpu_batch)
                and all(a.data.contiguous for a in targets_cpu_batch)
            ):
                print("WARNING! Non-contiguous arrays encountered. Shape:", predictions_cpu_batch[0].shape)
                global ENCOUNTERED_NONCONTIGUOUS
                ENCOUNTERED_NONCONTIGUOUS = True
            predictions_cpu_batch = [np.ascontiguousarray(a) for a in predictions_cpu_batch]
            targets_cpu_batch = [np.ascontiguousarray(a) for a in targets_cpu_batch]

            barcodes_batch = betti_matching.compute_barcode(predictions_cpu_batch + targets_cpu_batch)
            barcodes_predictions, barcodes_targets = (
                barcodes_batch[: len(barcodes_batch) // 2],
                barcodes_batch[len(barcodes_batch) // 2 :],
            )

            for barcode_prediction, barcode_target in zip(barcodes_predictions, barcodes_targets):
                losses.append(
                    self._wasserstein_loss(
                        prediction[current_instance_index].squeeze(0),
                        target[current_instance_index].squeeze(0),
                        barcode_prediction,
                        barcode_target,
                    )
                )
                current_instance_index += 1

        return torch.mean(torch.concatenate(losses))

    def _wasserstein_loss(
        self,
        prediction: torch.Tensor,
        target: torch.Tensor,
        barcode_result_prediction: betti_matching.return_types.BarcodeResult,
        barcode_result_target: betti_matching.return_types.BarcodeResult,
    ) -> torch.Tensor:
        """Compute the squared‐L2 Wasserstein distance between two persistence diagrams."""

        dims = len(barcode_result_prediction.birth_coordinates)
        losses_by_dim = torch.zeros(dims, device=prediction.device, dtype=torch.float32)

        for dim in range(dims):
            (
                prediction_birth_coordinates,
                prediction_death_coordinates,
                target_birth_coordinates,
                target_death_coordinates,
            ) = [
                torch.tensor(array, device=prediction.device, dtype=torch.long)
                for array in [
                    barcode_result_prediction.birth_coordinates[dim],
                    barcode_result_prediction.death_coordinates[dim],
                    barcode_result_target.birth_coordinates[dim],
                    barcode_result_target.death_coordinates[dim],
                ]
            ]

            # (M, 2) tensor of persistence pairs for prediction
            prediction_pairs = torch.stack(
                [
                    prediction[tuple(coords[:, i] for i in range(coords.shape[1]))]
                    for coords in [prediction_birth_coordinates, prediction_death_coordinates]
                ],
                dim=1,
            )
            # (M, 2) tensor of persistence pairs for target
            target_pairs = torch.stack(
                [
                    target[tuple(coords[:, i] for i in range(coords.shape[1]))]
                    for coords in [target_birth_coordinates, target_death_coordinates]
                ],
                dim=1,
            )

            # TODO check if the adjustments to order=2 and internal_p=2 is correct
            _, matching = wasserstein.wasserstein_distance(
                prediction_pairs.detach().cpu(),
                target_pairs.detach().cpu(),
                order=2,
                internal_p=2,
                matching=True,
                keep_essential_parts=False,
            )  # type: ignore
            matching = torch.tensor(matching.reshape(-1, 2), device=prediction.device, dtype=torch.long)

            matched_pairs = matching[(matching[:, 0] >= 0) & (matching[:, 1] >= 0)]
            loss_matched = ((prediction_pairs[matched_pairs[:, 0]] - target_pairs[matched_pairs[:, 1]]) ** 2).sum()  # type: ignore
            prediction_pairs_unmatched = prediction_pairs[matching[matching[:, 1] == -1][:, 0]]
            target_pairs_unmatched = target_pairs[matching[matching[:, 0] == -1][:, 1]]
            loss_unmatched = 0.5 * (
                ((prediction_pairs_unmatched[:, 0] - prediction_pairs_unmatched[:, 1]) ** 2).sum()
                + ((target_pairs_unmatched[:, 0] - target_pairs_unmatched[:, 1]) ** 2).sum()
            )  # type: ignore

            losses_by_dim[dim] = loss_matched + loss_unmatched

        return torch.sum(losses_by_dim).reshape(1)
