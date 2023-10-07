# global
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np

import ivy

# local


def all(
    x: np.ndarray,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    try:
        return np.asarray(np.all(x, axis=axis, keepdims=keepdims, out=out))
    except np.AxisError as error:
        raise ivy.utils.exceptions.IvyIndexError(error)


all.support_native_out = True


def any(
    x: np.ndarray,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.asarray(np.any(x, axis=axis, keepdims=keepdims, out=out))


any.support_native_out = True
