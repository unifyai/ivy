"""Collection of Paddle random functions, wrapped to fit Ivy syntax and signature."""

# global
import paddle
from typing import Optional, Union, Sequence

# local
import ivy
from paddle.fluid.libpaddle import Place
from ivy.utils.exceptions import IvyNotImplementedException
from ivy.functional.backends.paddle.device import to_device
from ivy.functional.ivy.random import (
    _check_bounds_and_get_shape,
    _randint_check_dtype_and_bound,
)
from ivy.func_wrapper import with_unsupported_dtypes
from . import backend_version
# Extra #
# ------#


@with_unsupported_dtypes(
    {
        "2.4.2 and below": (
            "int8"
        )
    },
    backend_version,
)
def random_uniform(
    *,
    low: Union[float, paddle.Tensor] = 0.0,
    high: Union[float, paddle.Tensor] = 1.0,
    shape: Optional[Union[paddle.Tensor, ivy.NativeShape, Sequence[int]]] = None,
    dtype: paddle.dtype,
    device: Place,
    seed=None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if not dtype:
        dtype = ivy.default_int_dtype()
    dtype = ivy.as_native_dtype(dtype)
    low = paddle.cast(low, "float32") if isinstance(low, paddle.Tensor) else low
    high = paddle.cast(high, "float32") if isinstance(high, paddle.Tensor) else high
    shape = _check_bounds_and_get_shape(low, high, shape)
    # Set range and seed
    range = high - low
    if seed:
        _ = paddle.seed(seed)
    _retval = to_device(
        paddle.cast(
            paddle.uniform(shape or [1], min=0.0, max=1.0) * range + low,
            dtype),
        device
    )
    return _retval if shape else _retval.squeeze(axis=0)


def random_normal(
    *,
    mean: Union[float, paddle.Tensor] = 0.0,
    std: Union[float, paddle.Tensor] = 1.0,
    shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    dtype: paddle.dtype,
    seed: Optional[int] = None,
    device: Place,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def multinomial(
    population_size: int,
    num_samples: int,
    /,
    *,
    batch_size: int = 1,
    probs: Optional[paddle.Tensor] = None,
    replace: bool = True,
    device: Place,
    seed: Optional[int] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


@with_unsupported_dtypes(
    {
        "2.4.2 and below": (
            "int8",
        )
    },
    backend_version,
)
def randint(
    low: Union[int, paddle.Tensor],
    high: Union[int, paddle.Tensor],
    /,
    *,
    shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    device: Place,
    dtype: Optional[Union[paddle.dtype, ivy.Dtype]] = None,
    seed: Optional[int] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if not dtype:
        dtype = ivy.default_int_dtype()
    dtype = ivy.as_native_dtype(dtype)
    _randint_check_dtype_and_bound(low, high, dtype)
    low = paddle.cast(low, "float32") if isinstance(low, paddle.Tensor) else low
    high = paddle.cast(high, "float32") if isinstance(high, paddle.Tensor) else high
    shape = _check_bounds_and_get_shape(low, high, shape)
    range = high - low
    if seed:
        _ = paddle.seed(seed)
    _retval = to_device(
        paddle.cast(
            paddle.uniform(shape or [1], min=0.0, max=1.0) * range + low,
            dtype),
        device
    )
    return _retval if shape else _retval.squeeze(axis=0)


def seed(*, seed_value: int = 0) -> None:
    _ = paddle.seed(seed_value)


def shuffle(
    x: paddle.Tensor,
    /,
    *,
    seed: Optional[int] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if seed:
        _ = paddle.seed(seed)
    # Use numpy's permutation function to shuffle indices
    indices = paddle.to_tensor(np.random.permutation(x.shape[0]), dtype='int64')
    shuffled_x = paddle.index_select(x, indices)
    return shuffled_x

shuffle.support_native_out = True
