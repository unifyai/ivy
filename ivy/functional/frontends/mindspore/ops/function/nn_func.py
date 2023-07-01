"""Includes Mindspore Frontend functions listed in the TODO list
https://github.com/unifyai/ivy/issues/14951."""

import ivy
from ivy.func_wrapper import with_supported_dtypes
from ivy.functional.frontends.paddle.func_wrapper import to_ivy_arrays_and_back


@with_supported_dtypes({"2.0 and below": ("float16", "float32")}, "mindspore")
@to_ivy_arrays_and_back
def sigmoid(x):
    """
    Sigmoid activation function.
    The function is shown as follows:
    .. math::
        \text{Sigmoid}(x) = \frac{1}{1 + \exp(-x)}
    Args:
        x (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of
            additional dimensions, with float16 or float32 data type.
    Returns:
        Tensor, with the same type and shape as the `x`.
    """
    return ivy.divide(1, ivy.add(1, ivy.exp(-x)))
