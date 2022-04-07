"""
Collection of Ivy activation functions.
"""

from typing import Union, Optional

# local
import ivy
from ivy.framework_handler import current_framework as _cur_framework


# Extra #
# ------#

def relu(x: Union[ivy.Array, ivy.NativeArray])\
        -> ivy.Array:
    """
    Applies the rectified linear unit function element-wise.

     Parameters
     ----------
     x:
         input array


    Returns
    -------
    out:
       an array containing the rectified linear unit activation of each element in ``x``.

    Examples:
    >>> x = ivy.array([-1, 0, 1])
    >>> y = ivy.relu(x)
    >>> print(y)
    [-0.0, 0.0, 1.0]
    """
    return _cur_framework(x).relu(x)


def leaky_relu(x: Union[ivy.Array, ivy.NativeArray], alpha: Optional[float] = 0.2)\
        -> ivy.Array:
    """Applies the leaky rectified linear unit function element-wise.

    Parameters
    ----------
    x : ivy.Array or ivy.NativeArray
        Input array.
    alpha : float, default=0.2
        Negative slope for ReLU.

    Returns
    -------
    ivy.Array
        The input array with leaky relu applied element-wise.

    Examples:
    >>> x = ivy.array([0.39, -0.85])
    >>> y = ivy.leaky_relu(x)
    >>> print(y)
    [0.39, -0.17]

    """
    return _cur_framework(x).leaky_relu(x, alpha)


def gelu(x: Union[ivy.Array, ivy.NativeArray], approximate: bool = True)\
    -> ivy.Array:
    """
    Applies the Gaussian error linear unit (GELU) activation function.

    Parameters
    -----------
    x: 
        Input array.
    approximate: 
        Whether to approximate. Default: True.

    Returns
    -------
    out: 
        The input array with gelu applied element-wise on ``x``.

    Examples:
    >>> x = ivy.array([-1. , 0. , 1. ])
    >>> y = ivy.gelu(x, True)
    >>> print(y)
    [-0.5,  0. ,  0.5]

    """
    return _cur_framework(x).gelu(x, approximate)


def tanh(x):
    """
    Applies the tangent hyperbolic function element-wise.

    :param x: Input array.
    :type x: array
    :return: The input array with tanh applied element-wise.
    """
    return _cur_framework(x).tanh(x)


def sigmoid(x):
    """
    Applies the sigmoid function element-wise.

    :param x: Input array.
    :type x: array
    :return: The input array with sigmoid applied element-wise.
    """
    return _cur_framework(x).sigmoid(x)


def softmax(x, axis=-1):
    """
    Applies the softmax function element-wise.

    :param x: Input array.
    :type x: array
    :param axis: The dimension softmax would be performed on. The default is -1 which indicates the last dimension.
    :type axis: int, optional
    :return: The input array with softmax applied element-wise.
    """
    return _cur_framework(x).softmax(x, axis)


def softplus(x):
    """
    Applies the softplus function element-wise.

    :param x: Input array.
    :type x: array
    :return: The input array with softplus applied element-wise.
    """
    return _cur_framework(x).softplus(x)
