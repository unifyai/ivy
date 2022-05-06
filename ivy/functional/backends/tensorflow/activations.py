"""Collection of TensorFlow activation functions, wrapped to fit Ivy syntax and
signature."""

from typing import Optional

# global
import tensorflow as tf
from tensorflow.python.types.core import Tensor

# local
import ivy


def relu(x: Tensor, out: Optional[Tensor] = None) -> Tensor:
    ret = tf.nn.relu(x)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def leaky_relu(x: Tensor, alpha: Optional[float] = 0.2) -> Tensor:
    return tf.nn.leaky_relu(x, alpha)


<<<<<<< HEAD
def gelu(x: Tensor, approximate: bool =True)\
    -> Tensor:
    return tf.nn.gelu(x, approximate)
    
=======
gelu = lambda x, approximate=True: tf.nn.gelu(x, approximate)


def sigmoid(x: Tensor) -> Tensor:
    return tf.nn.sigmoid(x)


<<<<<<< HEAD
>>>>>>> 464f96bfbef0c7b408a6fe23783748f2e2b83eb5
def tanh(x: Tensor)\
        -> Tensor:
=======
def tanh(x: Tensor) -> Tensor:
>>>>>>> 11942b2457e1f0e7da7cb175a838a4347ef9e0f5
    return tf.nn.tanh(x)


def softmax(x: Tensor, axis: Optional[int] = -1) -> Tensor:
    return tf.nn.softmax(x, axis)


def softplus(x: Tensor) -> Tensor:
    return tf.nn.softplus(x)
