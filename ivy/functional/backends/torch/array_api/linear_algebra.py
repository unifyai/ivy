# global
import torch
from typing import Union, Optional, Tuple, Literal, List

# local
from ivy import inf


def vector_norm(x: torch.Tensor,
                p: Union[int, float, Literal[inf, - inf]] = 2,
                axis: Optional[Union[int, Tuple[int]]] = None,
                keepdims: bool = False)\
        -> torch.Tensor:

    py_normalized_vector = torch.linalg.vector_norm(x, p, axis, keepdims)

    if py_normalized_vector.shape == ():
        return torch.unsqueeze(py_normalized_vector, 0)

    return py_normalized_vector


def diagonal(x: torch.Tensor,
             offset: int = 0,
             axis1: int = -2,
             axis2: int = -1) -> torch.Tensor:
    return torch.diagonal(x, offset=offset, dim1=axis1, dim2=axis2)


def tensordot(x1: torch.Tensor, x2: torch.Tensor,
              axes: Union[int, Tuple[List[int], List[int]]] = 2) \
        -> torch.Tensor:

    # find the type to promote to
    dtype = torch.promote_types(x1.dtype, x2.dtype)
    # type conversion to one that torch.tensordot can work with
    x1, x2 = x1.type(torch.float32), x2.type(torch.float32)

    # handle tensordot for axes==0
    # otherwise call with axes
    if axes == 0:
        return (x1.reshape(x1.size() + (1,) * x2.dim()) * x2).type(dtype)
    return torch.tensordot(x1, x2, dims=axes).type(dtype)
