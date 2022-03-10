# global
from typing import Union, Optional, Tuple, Literal
from ivy.framework_handler import current_framework as _cur_framework

# local
import ivy
from ivy.framework_handler import current_framework as _cur_framework
inf = float('inf')


# noinspection PyShadowingBuiltins
def vector_norm(x: Union[ivy.Array, ivy.NativeArray],
                axis: Optional[Union[int, Tuple[int]]] = None,
                keepdims: bool = False,
                ord: Union[int, float, Literal[inf, -inf]] = 2)\
        -> ivy.Array:

    """
    Computes the vector norm of a vector (or batch of vectors) ``x``.

    Parameters
    ----------
    x:
        input array. Should have a floating-point data type.
    axis:
        If an integer, ``axis`` specifies the axis (dimension) along which to compute vector norms. If an n-tuple, ``axis`` specifies the axes (dimensions) along which to compute batched vector norms. If ``None``, the vector norm must be computed over all array values (i.e., equivalent to computing the vector norm of a flattened array). Negative indices must be supported. Default: ``None``.
    keepdims:
        If ``True``, the axes (dimensions) specified by ``axis`` must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the axes (dimensions) specified by ``axis`` must not be included in the result. Default: ``False``.
    ord:
        order of the norm. The following mathematical norms must be supported:
        +------------------+----------------------------+
        | ord              | description                |
        +==================+============================+
        | 1                | L1-norm (Manhattan)        |
        +------------------+----------------------------+
        | 2                | L2-norm (Euclidean)        |
        +------------------+----------------------------+
        | inf              | infinity norm              |
        +------------------+----------------------------+
        | (int,float >= 1) | p-norm                     |
        +------------------+----------------------------+
        The following non-mathematical "norms" must be supported:
        +------------------+--------------------------------+
        | ord              | description                    |
        +==================+================================+
        | 0                | sum(a != 0)                    |
        +------------------+--------------------------------+
        | -1               | 1./sum(1./abs(a))              |
        +------------------+--------------------------------+
        | -2               | 1./sqrt(sum(1./abs(a)\*\*2))   |
        +------------------+--------------------------------+
        | -inf             | min(abs(a))                    |
        +------------------+--------------------------------+
        | (int,float < 1)  | sum(abs(a)\*\*ord)\*\*(1./ord) |
        +------------------+--------------------------------+
        Default: ``2``.

    Returns
    -------
    out:
        an array containing the vector norms. If ``axis`` is ``None``, the returned array must be a zero-dimensional array containing a vector norm. If ``axis`` is a scalar value (``int`` or ``float``), the returned array must have a rank which is one less than the rank of ``x``. If ``axis`` is a ``n``-tuple, the returned array must have a rank which is ``n`` less than the rank of ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.
    """

    if ord == -float('inf'):
        return ivy.reduce_min(ivy.abs(x), axis, keepdims)
    elif ord == float('inf'):
        return ivy.reduce_max(ivy.abs(x), axis, keepdims)
    elif ord == 0:
        return ivy.reduce_sum(ivy.cast(x != 0, 'float32'), axis, keepdims)
    x_raised = x ** ord
    return ivy.reduce_sum(x_raised, axis, keepdims) ** (1/ord)

def svd(x:Union[ivy.Array,ivy.NativeArray],full_matrices: bool = True)->Union[ivy.Array, Tuple[ivy.Array,...]]:

    """
    Singular Value Decomposition.
    When x is a 2D array, it is factorized as u @ numpy.diag(s) @ vh = (u * s) @ vh, where u and vh are 2D unitary
    arrays and s is a 1D array of a’s singular values. When x is higher-dimensional, SVD is applied in batched mode.

    :param x: Input array with number of dimensions >= 2.
    :type x: array
    :return:
        u -> { (…, M, M), (…, M, K) } array \n
        Unitary array(s). The first (number of dims - 2) dimensions have the same size as those of the input a.
        The size of the last two dimensions depends on the value of full_matrices.

        s -> (…, K) array \n
        Vector(s) with the singular values, within each vector sorted in descending ord.
        The first (number of dims - 2) dimensions have the same size as those of the input a.

        vh -> { (…, N, N), (…, K, N) } array \n
        Unitary array(s). The first (number of dims - 2) dimensions have the same size as those of the input a.
        The size of the last two dimensions depends on the value of full_matrices.
    """
    return _cur_framework(x).svd(x,full_matrices)

def diagonal(x: ivy.Array,
             offset: int = 0,
             axis1: int = -2,
             axis2: int = -1) -> ivy.Array:
    """
    Returns the specified diagonals of a matrix (or a stack of matrices) ``x``.
    Parameters
    ----------
    x:
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.
    offset:
        offset specifying the off-diagonal relative to the main diagonal.
        - ``offset = 0``: the main diagonal.
        - ``offset > 0``: off-diagonal above the main diagonal.
        - ``offset < 0``: off-diagonal below the main diagonal.
        Default: `0`.
    axis1:
        axis to be used as the first axis of the 2-D sub-arrays from which the diagonals should be taken.
        Defaults to first axis (0).
    axis2:
        axis to be used as the second axis of the 2-D sub-arrays from which the diagonals should be taken.
        Defaults to second axis (1).

    Returns
    -------
    out:
        an array containing the diagonals and whose shape is determined by removing the last two dimensions and appending a dimension equal to the size of the resulting diagonals. The returned array must have the same data type as ``x``.
    """
    return _cur_framework(x).diagonal(x, offset, axis1=axis1, axis2=axis2)

def cross(x1: Union[ivy.Array, ivy.NativeArray], x2: Union[ivy.Array, ivy.NativeArray],
          axis: Optional[int] = -1) -> ivy.Array:
    """
    Compute and return the cross product of 3-element vectors, it must have the same shape as b
    :param axis: the axis (dimension) of a and b containing the vector for which to compute the cross
    product default is -1
    :type  axis: int
    :param x1: first input, should have a numeric data type
    :type x1: array
    :param x2: second input, should have a numeric data type
    :type x2: array
    :return: an array that contains the cross products
    """
    return _cur_framework(x1).cross(x1, x2, axis)
