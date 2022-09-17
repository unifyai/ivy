"""Collection of Jax activation functions, wrapped to fit Ivy syntax and signature."""

# global
import jax
import jax.numpy as jnp
from typing import Optional, Union

# local
from ivy.functional.backends.jax import JaxArray


def gelu(
    x: JaxArray,
    /,
    *,
    approximate: bool = True,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jax.nn.gelu(x, approximate)


def leaky_relu(
    x: JaxArray, /, *, alpha: float = 0.2, out: Optional[JaxArray] = None
) -> JaxArray:
    return jnp.where(x > 0, x, x * alpha)


def relu(x: JaxArray, /, *, out: Optional[JaxArray] = None) -> JaxArray:
    return jnp.maximum(x, 0)


def sigmoid(x: JaxArray, /, *, out: Optional[JaxArray] = None) -> JaxArray:
    return 1 / (1 + jnp.exp(-x))


def softmax(
    x: JaxArray, /, *, axis: Optional[int] = None, out: Optional[JaxArray] = None
) -> JaxArray:
    if axis is None:
        axis = -1
    return jax.nn.softmax(x, axis)


def softplus(x: JaxArray,
             /,
             *,
             beta: Optional[Union[int, float, None]] = None,
             threshold: Optional[Union[int, float]] = 20,
             out: Optional[JaxArray] = None) -> JaxArray:

    if beta is not None and beta != 1:
        res = (jnp.log1p(jnp.exp(-jnp.abs(x * beta)))
               + jnp.maximum(x * beta, 0)) / beta
        return np.where(x * beta > threshold, x, res)
    else:
        res = (jnp.log1p(jnp.exp(-jnp.abs(x))) + jnp.maximum(x, 0))
        return np.where(x > threshold, x, res)
