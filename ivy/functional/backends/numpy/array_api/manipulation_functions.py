# global
import numpy as np
from typing import Union, Tuple, Optional, List


def flip(x: np.ndarray,
         axis: Optional[Union[int, Tuple[int], List[int]]] = None)\
         -> np.ndarray:
    num_dims = len(x.shape)
    if not num_dims:
        return x
    if axis is None:
        axis = list(range(num_dims))
    if type(axis) is int:
        axis = [axis]
    axis = [item + num_dims if item < 0 else item for item in axis]
    return np.flip(x, axis)

def stack(x: Union[np.ndarray, Tuple[np.ndarray], List[np.ndarray]],
          axis: Optional[int] = None)\
          -> np.ndarray:
    if x is np.ndarray:
        x = [x]
    if axis is None:
        axis = 0
    return np.stack(x, axis)
