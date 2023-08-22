# global
from typing import Union, Optional

# local
import ivy
from ivy.func_wrapper import (
    handle_nestable,
    inputs_to_ivy_arrays,
    handle_array_like_without_promotion,
    handle_array_function,
)
from ivy.utils.exceptions import handle_exceptions


# log_poisson_loss
@handle_exceptions
@handle_nestable
@inputs_to_ivy_arrays
@handle_array_function
def log_poisson_loss(
    true: Union[ivy.Array, ivy.NativeArray],
    pred: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    compute_full_loss: bool = False,
    axis: int = -1,
    reduction: str = "none",
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """
    Compute the log-likelihood loss between the prediction and the target under the
    assumption that the target has a Poisson distribution. Caveat: By default, this is
    not the exact loss, but the loss minus a constant term [log(z!)]. That has no effect
    for optimization, but does not play well with relative loss comparisons. To compute
    an approximation of the log factorial term, specify ``compute_full_loss=True`` to
    enable Stirling's Approximation.

    Parameters
    ----------
    true
        input array containing true labels.
    pred
        input array containing Predicted labels.
    compute_full_loss
        whether to compute the full loss. If false, a constant term is dropped
        in favor of more efficient optimization. Default: ``False``.
    axis
        the axis along which to compute the log-likelihood loss. If axis is ``-1``,
        the log-likelihood loss will be computed along the last dimension.
        Default: ``-1``.
    reduction
        ``'none'``: No reduction will be applied to the output.
        ``'mean'``: The output will be averaged.
        ``'sum'``: The output will be summed. Default: ``'none'``.
    out
        optional output array, for writing the result to. It must have a shape
        that the inputs broadcast to.

    Returns
    -------
    ret
        The binary log-likelihood loss between the given distributions.


    Examples
    --------
    >>> x = ivy.array([0, 0, 1, 0])
    >>> y = ivy.array([0.25, 0.25, 0.25, 0.25])
    >>> print(ivy.log_poisson_loss(x, z))
    ivy.array([1.28402555, 1.28402555, 1.03402555, 1.28402555])

    >>> z = ivy.array([0.1, 0.1, 0.7, 0.1])
    >>> print(ivy.log_poisson_loss(x, z, reduction='mean'))
    ivy.array(1.1573164)
    """
    try:
        assert true.shape == pred.shape
    except ValueError:
        raise ValueError(
            "`pred` and `true` must have the same shape, received "
            f"({pred.shape} vs {true.shape})."
        )

    loss = ivy.exp(pred) - pred * true
    if compute_full_loss:
        stirling_approx = (
            (true * ivy.log(true)) - true + (0.5 * ivy.log(2 * ivy.pi * true))
        )
        cond = ivy.logical_and(true >= 0.0, true <= 1.0)
        loss += ivy.where(cond, ivy.zeros_like(loss), stirling_approx)
    if reduction == "sum":
        return ivy.sum(loss, axis=axis, out=out)
    elif reduction == "mean":
        return ivy.mean(loss, axis=axis, out=out)
    else:
        return ivy.inplace_update(out, loss) if out is not None else loss


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_ivy_arrays
@handle_array_function
def l1_loss(
    input: Union[ivy.Array, ivy.NativeArray],
    target: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    reduction: Optional[str] = "mean",
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """
    Compute L1 loss (Mean Absolute Error - MAE) between targeticted and input values.

    Parameters
    ----------
    input : Union[ivy.Array, ivy.NativeArray]
        Input array containing input values.
    target : Union[ivy.Array, ivy.NativeArray]
        Input array containing targeted values.
    reduction : str, optional
        Reduction method for the output loss. Options:
        "none" (no reduction), "mean" (mean of losses),
        "sum" (sum of losses). Default: "mean".
    out : Optional[ivy.Array], optional
        Optional output array for writing the result to.
        It must have a shape that the inputs broadcast to.


    Returns
    -------
    ivy.Array
        The L1 loss (MAE) between the given input and targeticted values.


    Examples
    --------
    >>> x = ivy.array([1.0, 2.0, 3.0])
    >>> y = ivy.array([0.5, 2.5, 2.0])
    >>> print(ivy.l1_loss(x, y))
    ivy.array(0.6)
    >>> a = ivy.array([[1.0, 2.0], [3.0, 4.0]])
    >>> b = ivy.array([[0.5, 1.5], [2.5, 3.5]])
    >>> print(ivy.l1_loss(a, b))
    ivy.array(0.5)
    """
    loss = ivy.abs(target - input)

    if reduction == "sum":
        return ivy.sum(loss, out=out)
    elif reduction == "mean":
        return ivy.mean(loss, out=out)
    else:
        return ivy.inplace_update(out, loss) if out is not None else loss


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_ivy_arrays
@handle_array_function
def smooth_l1_loss(
    input: Union[ivy.Array, ivy.NativeArray],
    target: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    beta: Optional[float] = 1.0,
    reduction: Optional[str] = "mean",
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """
    Compute the smooth L1 loss between two input tensors.

    Parameters
    ----------
    input : array_like
        First input tensor.
    target : array_like
        Second input tensor.
    beta : float, optional
        The smooth parameter. Default is 1.0.
    reduction : str, optional
        Specifies the type of reduction to apply to the output.
        Should be one of 'none', 'sum', or 'mean'. Default is 'mean'.
    out : array, optional
        Optional output array, for writing the result to.
        It must have a shape that the inputs broadcast to.

    Returns
    -------
    ret : array
        The smooth_l1_loss between the two input tensors.

    Examples
    --------
    >>> input = ivy.array([1.0, 2.0, 3.0])
    >>> target = ivy.array([2.5, 1.8, 3.2])
    >>> ivy.smooth_l1_loss(x, y, beta=1.0)
    ivy.array(0.3467)
    >>> input = ivy.array([1.0, 2.0, 3.0])
    >>> target = ivy.array([6.0, 2.0, 3.0])
    >>> ivy.smooth_l1_loss(x, y, beta=1.0)
    ivy.array(1.5)

    Smooth L1 loss defined in the Fast R-CNN paper as:
    ::
                      | 0.5 * x ** 2 / beta   if abs(x) < beta
        smoothl1(x) = |
                      | abs(x) - 0.5 * beta   otherwise,

    where x = input - target.

    Smooth L1 loss is related to Huber loss, which is defined as:
    ::
                    | 0.5 * x ** 2                  if abs(x) < beta
         huber(x) = |
                    | beta * (abs(x) - 0.5 * beta)  otherwise

    Smooth L1 loss is equal to huber(x) / beta. This leads to the following
    differences:

     - As beta -> 0, Smooth L1 loss converges to L1 loss, while Huber loss
       converges to a constant 0 loss.
     - As beta -> +inf, Smooth L1 converges to a constant 0 loss, while Huber loss
       converges to L2 loss.
     - For Smooth L1 loss, as beta varies, the L1 segment of the loss has a constant
       slope of 1. For Huber loss, the slope of the L1 segment is beta.

    Smooth L1 loss can be seen as exactly L1 loss, but with the abs(x) < beta
    portion replaced with a quadratic function such that at abs(x) = beta, its
    slope is 1. The quadratic segment smooths the L1 loss near x = 0.


        input (Tensor): input tensor of any shape
        target (Tensor): target value tensor with the same shape as input
        beta (float): L1 to L2 change point.
            For beta values < 1e-5, L1 loss is computed.
        reduction: 'none' | 'mean' | 'sum'
                 'none': No reduction will be applied to the output.
                 'mean': The output will be averaged.
                 'sum': The output will be summed.


        The loss with the reduction option applied.
    """
    if beta < 1e-5:
        # if beta == 0,  will result in nan gradients when
        # the chain rule is applied due to pytorch implementation details
        # (the False branch "0.5 * n ** 2 / 0" has an incoming gradient of
        # zeros, rather than "no gradient"). To avoid this issue, we define
        # small values of beta to be exactly l1 loss.
        loss = ivy.abs(input - target)
    else:
        n = ivy.abs(input - target)
        cond = n < beta
        loss = ivy.where(cond, 0.5 * n**2 / beta, n - 0.5 * beta)

    if reduction == "mean":
        return ivy.mean(loss, out=out)
    elif reduction == "sum":
        return ivy.sum(loss, out=out)
    elif reduction == "none":
        return ivy.inplace_update(out, loss) if out is not None else loss
