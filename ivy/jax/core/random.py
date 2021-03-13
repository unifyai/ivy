"""
Collection of Jax random functions, wrapped to fit Ivy syntax and signature.
"""

# global
import jax as _jax

# local
from ivy.jax.core.general import _to_dev

RNG = _jax.random.PRNGKey(0)


def random_uniform(low=0.0, high=1.0, shape=None, dev_str='cpu'):
    global RNG
    RNG, rng_input = _jax.random.split(RNG)
    return _to_dev(_jax.random.uniform(rng_input, shape if shape else (), minval=low, maxval=high), dev_str)


def randint(low, high, shape, dev_str='cpu'):
    global RNG
    RNG, rng_input = _jax.random.split(RNG)
    return _to_dev(_jax.random.randint(rng_input, shape, low, high), dev_str)


def seed(seed_value=0):
    global RNG
    RNG = _jax.random.PRNGKey(seed_value)
    return


def shuffle(x):
    global RNG
    RNG, rng_input = _jax.random.split(RNG)
    return _jax.random.shuffle(rng_input, x)
