import ivy
import numpy as np
from typing import Optional
from ivy.functional.backends.numpy.helpers import _scalar_output_to_0d_array
from ivy.func_wrapper import (
    with_unsupported_dtypes,
    with_supported_device_and_dtypes,
)
from . import backend_version


@with_unsupported_dtypes({"1.26.0 and below": ("bool",)}, backend_version)
@_scalar_output_to_0d_array
def huber_loss(
    input: np.ndarray,
    target: np.ndarray,
    /,
    *,
    delta: Optional[float] = 1.0,
    reduction: Optional[str] = "mean",
) -> np.ndarray:
    abs_diff = np.abs(input - target)
    quadratic_loss = 0.5 * (abs_diff**2)
    linear_loss = delta * (abs_diff - 0.5 * delta)
    loss = np.where(abs_diff <= delta, quadratic_loss, linear_loss)

    if reduction == "sum":
        return np.sum(loss)
    elif reduction == "mean":
        return np.mean(loss)
    else:
        return loss


# Implementation of smooth_l1_loss in the given format
@with_unsupported_dtypes({"1.26.0 and below": ("bool",)}, backend_version)
@_scalar_output_to_0d_array
def smooth_l1_loss(
    input: np.ndarray,
    target: np.ndarray,
    /,
    *,
    beta: Optional[float] = 1.0,
    reduction: Optional[str] = "mean",
) -> np.ndarray:
    if beta < 1e-5:
        loss = np.abs(input - target)
    else:
        diff = np.abs(input - target)
        loss = np.where(diff < beta, 0.5 * diff**2 / beta, diff - 0.5 * beta)

    if reduction == "mean":
        return np.mean(loss)
    elif reduction == "sum":
        return np.sum(loss)
    else:
        return loss


@with_unsupported_dtypes({"1.26.0 and below": ("bool",)}, backend_version)
@_scalar_output_to_0d_array
def soft_margin_loss(
    input: np.ndarray,
    target: np.ndarray,
    /,
    *,
    reduction: Optional[str] = "mean",
) -> np.ndarray:
    loss = np.sum(np.log1p(np.exp(-input * target))) / input.size

    if reduction == "mean":
        return np.mean(loss)
    elif reduction == "sum":
        return np.sum(loss)
    else:
        return loss


def _apply_loss_reduction(loss: np.ndarray, reduction: str, axis, out) -> np.ndarray:
    if reduction == "sum":
        return np.sum(loss, axis=axis, out=out)
    elif reduction == "mean":
        return np.mean(loss, axis=axis, out=out)
    else:  # reduction == "none"
        if out is not None:
            out[...] = loss
            return out
        return loss


def _validate_poisson_nll_params(
    input,
    label,
    epsilon,
    reduction,
    allowed_dtypes=["float16", "float32", "float64"],
):
    # Validate dtypes
    for parameter, name in zip([input, label], ["input", "label"]):
        if parameter.dtype not in allowed_dtypes:
            raise ValueError(
                "The dtype of '%s' in poisson_nll_loss should be one of %s, but"
                " received %s." % (name, allowed_dtypes, parameter.dtype)
            )

    # Validate epsilon
    if epsilon <= 0:
        raise ValueError(
            "The value of `epsilon` in poisson_nll_loss should be positive, but"
            " received %f, which is not allowed" % epsilon
        )

    # Validate reduction
    if reduction not in ["sum", "mean", "none"]:
        raise ValueError(
            "The value of 'reduction' in poisson_nll_loss should be 'sum', 'mean' or"
            " 'none', but received %s, which is not allowed." % reduction
        )

    # Validate shape
    if input.shape != label.shape:
        raise ValueError(
            "The shape of 'input' (%s) must be the same as the shape of 'label' (%s)."
            % (input.shape, label.shape)
        )

    return True


@with_supported_device_and_dtypes(
    {
        "1.25.2 and below": {
            "cpu": ("float16", "float32", "float64"),
        }
    },
    backend_version,
)
@_scalar_output_to_0d_array
def poisson_nll_loss(
    input: np.ndarray,
    target: np.ndarray,
    *,
    log_input: bool = True,
    full: bool = False,
    eps: float = 1e-8,
    reduction: str = "mean",
) -> np.ndarray:
    input_arr = np.asarray(input)
    target_arr = np.asarray(target, dtype=input.dtype)

    _validate_poisson_nll_params(input_arr, target_arr, eps, reduction)

    if log_input:
        loss = np.exp(input_arr) - target_arr * input_arr
    else:
        loss = input_arr - target_arr * np.log(input_arr + eps)

    if full:
        point_five = np.array(0.5, dtype=target_arr.dtype)
        two_pi = np.array(2 * np.pi, dtype=target_arr.dtype)
        striling_approx_term = (
            (target_arr * np.log(target_arr))
            - target_arr
            + (point_five * np.log(two_pi * target_arr))
        )
        zeroes = np.zeros_like(target_arr, dtype=target_arr.dtype)
        ones = np.ones_like(target_arr, dtype=target_arr.dtype)
        cond = np.logical_and(target_arr >= zeroes, target_arr <= ones)
        loss = loss + np.where(cond, zeroes, striling_approx_term)
    return _apply_loss_reduction(loss, reduction)


@with_supported_device_and_dtypes(
    {
        "1.25.2 and below": {
            "cpu": ("float16", "float32", "float64"),
        }
    },
    backend_version,
)
@_scalar_output_to_0d_array
def binary_cross_entropy(
    input: np.ndarray,
    target: np.ndarray,
    /,
    *,
    from_logits: bool = False,
    epsilon: float = 1e-7,
    reduction: str = "none",
    pos_weight: Optional[np.ndarray] = None,
    axis: Optional[int] = None,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    input_arr = np.asarray(input)
    target_arr = np.asarray(target, dtype=input.dtype)

    if not (0.0 <= epsilon <= 1e-5):
        raise ValueError("epsilon should be a float in [0, 1e-5]")

    if not from_logits and pos_weight is not None:
        raise ValueError("pos_weight is only allowed when from_logits is set to True")

    if from_logits:
        input = 1.0 / 1.0 + np.exp(-input_arr)
        if pos_weight is not None:
            pos_weight = np.asarray(pos_weight, dtype=input.dtype)
            num_classes = (
                input_arr.shape[0] if len(input_arr.shape) == 1 else input_arr.shape[1]
            )
            if pos_weight.shape[0] != num_classes:
                raise ValueError(
                    "pos_weight must have the same size as the number of classes in"
                    " pred at non-singleton dimension 1"
                )
            loss = -1.0 * (
                (pos_weight * target_arr * np.log(input_arr + epsilon))
                + (1.0 - target_arr) * np.log(1.0 - input_arr + epsilon)
            )
        else:
            loss = -1.0 * (
                target_arr * np.log(input_arr)
                + (1.0 - target_arr) * np.log(1.0 - input_arr)
            )
    else:
        loss = -1.0 * (
            target_arr * np.log(input_arr)
            + (1.0 - target_arr) * np.log(1.0 - input_arr)
        )
    return _apply_loss_reduction(loss, reduction, axis=axis, out=out)


@with_supported_device_and_dtypes(
    {
        "1.25.2 and below": {
            "cpu": ("float16", "float32", "float64"),
        }
    },
    backend_version,
)
@_scalar_output_to_0d_array
def cross_entropy(
    input: np.ndarray,
    target: np.ndarray,
    /,
    *,
    axis: int = -1,
    epsilon: float = 1e-7,
    reduction: str = "none",
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    ivy.utils.assertions.check_elem_in_list(reduction, ["none", "sum", "mean"])
    input = np.clip(input, epsilon, 1 - epsilon)
    loss = np.log(input) * target
    return _apply_loss_reduction(loss, reduction, axis, out)
