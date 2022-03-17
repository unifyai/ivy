# global
import jax
import jax.numpy as jnp
from typing import Union, Optional, Tuple, Literal
from collections import namedtuple

# local
from ivy import inf
from ivy.functional.backends.jax import JaxArray
import ivy


def matrix_transpose(x: JaxArray)\
        -> JaxArray:
    return jnp.swapaxes(x, -1, -2)


# noinspection PyUnusedLocal,PyShadowingBuiltins
def vector_norm(x: JaxArray,
                axis: Optional[Union[int, Tuple[int]]] = None, 
                keepdims: bool = False,
                ord: Union[int, float, Literal[inf, -inf]] = 2)\
        -> JaxArray:

    if axis is None:
        jnp_normalized_vector = jnp.linalg.norm(jnp.ravel(x), ord, axis, keepdims)
    else:
        jnp_normalized_vector = jnp.linalg.norm(x, ord, axis, keepdims)

    if jnp_normalized_vector.shape == ():
        return jnp.expand_dims(jnp_normalized_vector, 0)
    return jnp_normalized_vector




def outer(x1: JaxArray,
          x2: JaxArray)\
        -> JaxArray:
    return jnp.outer(x1,x2)

  
def svd(x:JaxArray,full_matrices: bool = True) -> Union[JaxArray, Tuple[JaxArray,...]]:
    results=namedtuple("svd", "U S Vh")
    U, D, VT=jnp.linalg.svd(x, full_matrices=full_matrices)
    res=results(U, D, VT)
    return res


def diagonal(x: JaxArray,
             offset: int = 0,
             axis1: int = -2,
             axis2: int = -1) -> JaxArray:
    return jnp.diagonal(x, offset, axis1, axis2)


def svdvals(x: JaxArray) -> JaxArray:
    return jnp.linalg.svd(x, compute_uv=False)


def qr(x: JaxArray,
       mode: str = 'reduced') -> namedtuple('qr', ['Q', 'R']):
    res = namedtuple('qr', ['Q', 'R'])
    q, r = jnp.linalg.qr(x, mode=mode)
    return res(q, r)


def matmul(a1: JaxArray,
           a2: JaxArray) -> JaxArray:
    return jnp.matmul(a1, a2)


def slogdet(x:Union[ivy.Array,ivy.NativeArray],full_matrices: bool = True) -> Union[ivy.Array, Tuple[ivy.Array,...]]:
    results = namedtuple("slogdet", "sign logabsdet")
    sign, logabsdet = jnp.linalg.slogdet(x)
    res = results(sign, logabsdet)
    return res


def trace(x: JaxArray,
          offset: int = 0)\
              -> JaxArray:
    return jax.numpy.trace(x, offset)
