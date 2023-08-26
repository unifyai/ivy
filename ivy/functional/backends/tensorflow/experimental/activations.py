from typing import Optional, Union

# global
import tensorflow as tf
from tensorflow.python.types.core import Tensor

# local
import ivy
from ivy.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from . import backend_version


def logit(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    eps: Optional[float] = None,
    out: Optional[Tensor] = None,
) -> Tensor:
    x_dtype = x.dtype
    if eps is None:
        x = tf.where(tf.math.logical_or(x > 1, x < 0), ivy.nan, x)
    else:
        x = tf.clip_by_value(x, eps, 1 - eps)
    return tf.cast(tf.math.log(x / (1 - x)), x_dtype)


@with_unsupported_dtypes({"2.13.0 and below": ("complex", "bool")}, backend_version)
def thresholded_relu(
    x: Tensor,
    /,
    *,
    threshold: Union[int, float] = 0,
    out: Optional[Tensor] = None,
) -> Tensor:
    threshold = tf.cast(threshold, x.dtype)
    return tf.cast(tf.where(x > threshold, x, 0), x.dtype)


def relu6(x: Tensor, /, *, out: Optional[Tensor] = None, complex_mode="jax") -> Tensor:
    return tf.nn.relu6(x)


def logsigmoid(
    input: Tensor, /, *, out: Optional[Tensor] = None, complex_mode="jax"
) -> Tensor:
    if input.dtype in [tf.complex64, tf.complex128]:
        return tf.math.log(tf.nn.sigmoid(input))
    return tf.math.log_sigmoid(input)


@with_supported_dtypes({"2.13.0 and below": ("float", "complex")}, backend_version)
def selu(x: Tensor, /, *, out: Optional[Tensor] = None, complex_mode="jax") -> Tensor:
    ret = tf.nn.selu(x)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret).astype(x.dtype)
    return ivy.astype(ret, x.dtype)


def silu(x: Tensor, /, *, out: Optional[Tensor] = None, complex_mode="jax") -> Tensor:
    ret = tf.nn.silu(x)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret).astype(x.dtype)
    return ivy.astype(ret, x.dtype)


@with_supported_dtypes({"2.13.0 and below": ("float", "complex")}, backend_version)
def elu(
    x: Tensor,
    /,
    *,
    alpha: float = 1.0,
    out: Optional[Tensor] = None,
    complex_mode="jax",
) -> Tensor:
    alpha = tf.cast(alpha, x.dtype)
    ret = tf.cast(tf.where(x > 0, x, tf.multiply(alpha, tf.math.expm1(x))), x.dtype)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret).astype(x.dtype)
    return ivy.astype(ret, x.dtype)
