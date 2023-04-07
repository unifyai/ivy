# flake8: noqa
# global
from numbers import Number
from typing import Union, Tuple, Iterable


# local
import ivy
from ivy.utils.exceptions import handle_exceptions
import ivy.functional.frontends.jax as jax_frontend


# Constructing dtypes are required as ivy.<dtype>
# will change dynamically on the backend and may not be available
int8 = ivy.IntDtype("int8")
int16 = ivy.IntDtype("int16")
int32 = ivy.IntDtype("int32")
int64 = ivy.IntDtype("int64")
uint8 = ivy.UintDtype("uint8")
uint16 = ivy.UintDtype("uint16")
uint32 = ivy.UintDtype("uint32")
uint64 = ivy.UintDtype("uint64")
bfloat16 = ivy.FloatDtype("bfloat16")
float16 = ivy.FloatDtype("float16")
float32 = ivy.FloatDtype("float32")
float64 = ivy.FloatDtype("float64")
complex64 = ivy.ComplexDtype("complex64")
complex128 = ivy.ComplexDtype("complex128")
bool = ivy.Dtype("bool")

# jax-numpy casting table
jax_numpy_casting_table = {
    bool: [
        bool,
        int8,
        int16,
        int32,
        int64,
        uint8,
        uint16,
        uint32,
        uint64,
        float16,
        float32,
        float64,
        complex64,
        complex128,
        bfloat16,
    ],
    int8: [
        int8,
        int16,
        int32,
        int64,
        float16,
        float32,
        float64,
        complex64,
        complex128,
        bfloat16,
    ],
    int16: [
        int16,
        int32,
        int64,
        float32,
        float64,
        complex64,
        complex128,
    ],
    int32: [
        int32,
        int64,
        float64,
        complex128,
    ],
    int64: [
        int64,
        float64,
        complex128,
    ],
    uint8: [
        int16,
        int32,
        int64,
        uint8,
        uint16,
        uint32,
        uint64,
        float16,
        float32,
        float64,
        complex64,
        complex128,
        bfloat16,
    ],
    uint16: [
        int32,
        int64,
        uint16,
        uint32,
        uint64,
        float32,
        float64,
        complex64,
        complex128,
    ],
    uint32: [
        int64,
        uint32,
        uint64,
        float64,
        complex128,
    ],
    uint64: [
        uint64,
        float64,
        complex128,
    ],
    float16: [
        float16,
        float32,
        float64,
        complex64,
        complex128,
    ],
    float32: [
        float32,
        float64,
        complex64,
        complex128,
    ],
    float64: [
        float64,
        complex128,
    ],
    complex64: [complex64, ivy.complex128],
    complex128: [complex128],
    bfloat16: [
        bfloat16,
        float32,
        float64,
        complex64,
        complex128,
    ],
}


# jax-numpy type promotion table
# data type promotion
jax_promotion_table = {
    (bool, bool): bool,
    (bool, uint8): uint8,
    (bool, uint16): uint16,
    (bool, uint32): uint32,
    (bool, uint64): uint64,
    (bool, int8): int8,
    (bool, int16): int16,
    (bool, int32): int32,
    (bool, int64): int64,
    (bool, bfloat16): bfloat16,
    (bool, float16): float16,
    (bool, float32): float32,
    (bool, float64): float64,
    (bool, complex64): complex64,
    (bool, complex128): complex128,
    (uint8, bool): uint8,
    (uint8, uint8): uint8,
    (uint8, uint16): uint16,
    (uint8, uint32): uint32,
    (uint8, uint64): uint64,
    (uint8, int8): int16,
    (uint8, int16): int16,
    (uint8, int32): int32,
    (uint8, int64): int64,
    (uint8, bfloat16): bfloat16,
    (uint8, float16): float16,
    (uint8, float32): float32,
    (uint8, float64): float64,
    (uint8, complex64): complex64,
    (uint8, complex128): complex128,
    (uint16, bool): uint16,
    (uint16, uint8): uint16,
    (uint16, uint16): uint16,
    (uint16, uint32): uint32,
    (uint16, uint64): uint64,
    (uint16, int8): int32,
    (uint16, int16): int32,
    (uint16, int32): int32,
    (uint16, int64): int64,
    (uint16, bfloat16): bfloat16,
    (uint16, float16): float16,
    (uint16, float32): float32,
    (uint16, float64): float64,
    (uint16, complex64): complex64,
    (uint16, complex128): complex128,
    (uint32, bool): uint32,
    (uint32, uint8): uint32,
    (uint32, uint16): uint32,
    (uint32, uint32): uint32,
    (uint32, uint64): uint64,
    (uint32, int8): int64,
    (uint32, int16): int64,
    (uint32, int32): int64,
    (uint32, int64): int64,
    (uint32, bfloat16): bfloat16,
    (uint32, float16): float16,
    (uint32, float32): float32,
    (uint32, float64): float64,
    (uint32, complex64): complex64,
    (uint32, complex128): complex128,
    (uint64, bool): uint64,
    (uint64, uint8): uint64,
    (uint64, uint16): uint64,
    (uint64, uint32): uint64,
    (uint64, uint64): uint64,
    (uint64, int8): float64,
    (uint64, int16): float64,
    (uint64, int32): float64,
    (uint64, int64): float64,
    (uint64, bfloat16): bfloat16,
    (uint64, float16): float16,
    (uint64, float32): float32,
    (uint64, float64): float64,
    (uint64, complex64): complex64,
    (uint64, complex128): complex128,
    (int8, bool): int8,
    (int8, uint8): int16,
    (int8, uint16): int32,
    (int8, uint32): int64,
    (int8, uint64): float64,
    (int8, int8): int8,
    (int8, int16): int16,
    (int8, int32): int32,
    (int8, int64): int64,
    (int8, bfloat16): bfloat16,
    (int8, float16): float16,
    (int8, float32): float32,
    (int8, float64): float64,
    (int8, complex64): complex64,
    (int8, complex128): complex128,
    (int16, bool): int16,
    (int16, uint8): int16,
    (int16, uint16): int32,
    (int16, uint32): int64,
    (int16, uint64): float64,
    (int16, int8): int16,
    (int16, int16): int16,
    (int16, int32): int32,
    (int16, int64): int64,
    (int16, bfloat16): bfloat16,
    (int16, float16): float16,
    (int16, float32): float32,
    (int16, float64): float64,
    (int16, complex64): complex64,
    (int16, complex128): complex128,
    (int32, bool): int32,
    (int32, uint8): int32,
    (int32, uint16): int32,
    (int32, uint32): int64,
    (int32, uint64): float64,
    (int32, int8): int32,
    (int32, int16): int32,
    (int32, int32): int32,
    (int32, int64): int64,
    (int32, bfloat16): bfloat16,
    (int32, float16): float16,
    (int32, float32): float32,
    (int32, float64): float64,
    (int32, complex64): complex64,
    (int32, complex128): complex128,
    (int64, bool): int64,
    (int64, uint8): int64,
    (int64, uint16): int64,
    (int64, uint32): int64,
    (int64, uint64): float64,
    (int64, int8): int64,
    (int64, int16): int64,
    (int64, int32): int64,
    (int64, int64): int64,
    (int64, bfloat16): bfloat16,
    (int64, float16): float16,
    (int64, float32): float32,
    (int64, float64): float64,
    (int64, complex64): complex64,
    (int64, complex128): complex128,
    (bfloat16, bool): bfloat16,
    (bfloat16, uint8): bfloat16,
    (bfloat16, uint16): bfloat16,
    (bfloat16, uint32): bfloat16,
    (bfloat16, uint64): bfloat16,
    (bfloat16, int8): bfloat16,
    (bfloat16, int16): bfloat16,
    (bfloat16, int32): bfloat16,
    (bfloat16, int64): bfloat16,
    (bfloat16, bfloat16): bfloat16,
    (bfloat16, float16): float32,
    (bfloat16, float32): float32,
    (bfloat16, float64): float64,
    (bfloat16, complex64): complex64,
    (bfloat16, complex128): complex128,
    (float16, bool): float16,
    (float16, uint8): float16,
    (float16, uint16): float16,
    (float16, uint32): float16,
    (float16, uint64): float16,
    (float16, int8): float16,
    (float16, int16): float16,
    (float16, int32): float16,
    (float16, int64): float16,
    (float16, bfloat16): float32,
    (float16, float16): float16,
    (float16, float32): float32,
    (float16, float64): float64,
    (float16, complex64): complex64,
    (float16, complex128): complex128,
    (float32, bool): float32,
    (float32, uint8): float32,
    (float32, uint16): float32,
    (float32, uint32): float32,
    (float32, uint64): float32,
    (float32, int8): float32,
    (float32, int16): float32,
    (float32, int32): float32,
    (float32, int64): float32,
    (float32, bfloat16): float32,
    (float32, float16): float32,
    (float32, float32): float32,
    (float32, float64): float64,
    (float32, complex64): complex64,
    (float32, complex128): complex128,
    (float64, bool): float64,
    (float64, uint8): float64,
    (float64, uint16): float64,
    (float64, uint32): float64,
    (float64, uint64): float64,
    (float64, int8): float64,
    (float64, int16): float64,
    (float64, int32): float64,
    (float64, int64): float64,
    (float64, bfloat16): float64,
    (float64, float16): float64,
    (float64, float32): float64,
    (float64, float64): float64,
    (float64, complex64): complex128,
    (float64, complex128): complex128,
    (complex64, bool): complex64,
    (complex64, int8): complex64,
    (complex64, int16): complex64,
    (complex64, int32): complex64,
    (complex64, int64): complex64,
    (complex64, uint8): complex64,
    (complex64, uint16): complex64,
    (complex64, uint32): complex64,
    (complex64, uint64): complex64,
    (complex64, float16): complex64,
    (complex64, float32): complex64,
    (complex64, float64): complex128,
    (complex64, bfloat16): complex64,
    (complex64, complex64): complex64,
    (complex64, complex128): complex128,
    (complex128, bool): complex128,
    (complex128, int8): complex128,
    (complex128, int16): complex128,
    (complex128, int32): complex128,
    (complex128, int64): complex128,
    (complex128, uint8): complex128,
    (complex128, uint16): complex128,
    (complex128, uint32): complex128,
    (complex128, uint64): complex128,
    (complex128, float16): complex128,
    (complex128, float32): complex128,
    (complex128, float64): complex128,
    (complex128, bfloat16): complex128,
    (complex128, complex64): complex128,
    (complex128, complex128): complex128,
}


dtype_replacement_dict = {
    int64: int32,
    uint64: uint32,
    float64: float32,
    complex128: complex64,
}


@handle_exceptions
def promote_types_jax(
    type1: Union[ivy.Dtype, ivy.NativeDtype],
    type2: Union[ivy.Dtype, ivy.NativeDtype],
    /,
) -> ivy.Dtype:
    """
    Promotes the datatypes type1 and type2, returning the data type they promote to
    Parameters
    ----------
    type1
        the first of the two types to promote
    type2
        the second of the two types to promote
    Returns
    -------
    ret
        The type that both input types promote to
    """
    try:
        ret = jax_promotion_table[(ivy.as_ivy_dtype(type1), ivy.as_ivy_dtype(type2))]
    except KeyError:
        raise ivy.utils.exceptions.IvyException("these dtypes are not type promotable")
    return ret


def _handle_x64_promotion(d):
    if not jax_frontend.config.jax_enable_x64:
        d = dtype_replacement_dict[d] if d in dtype_replacement_dict else d
    return d


@handle_exceptions
def promote_types_of_jax_inputs(
    x1: Union[ivy.Array, Number, Iterable[Number]],
    x2: Union[ivy.Array, Number, Iterable[Number]],
    /,
) -> Tuple[ivy.Array, ivy.Array]:
    """
    Promotes the dtype of the given native array inputs to a common dtype
    based on type promotion rules. While passing float or integer values or any
    other non-array input to this function, it should be noted that the return will
    be an array-like object. Therefore, outputs from this function should be used
    as inputs only for those functions that expect an array-like or tensor-like objects,
    otherwise it might give unexpected results.
    """
    type1 = ivy.default_dtype(item=x1).strip("u123456789")
    type2 = ivy.default_dtype(item=x2).strip("u123456789")
    if hasattr(x1, "dtype") and not hasattr(x2, "dtype") and type1 == type2:
        x2 = ivy.asarray(
            x2, dtype=x1.dtype, device=ivy.default_device(item=x1, as_native=False)
        )
    elif not hasattr(x1, "dtype") and hasattr(x2, "dtype") and type1 == type2:
        x1 = ivy.asarray(
            x1, dtype=x2.dtype, device=ivy.default_device(item=x2, as_native=False)
        )
    else:
        x1 = ivy.asarray(x1)
        x2 = ivy.asarray(x2)
        x1_type, x2_type = x1.dtype, x2.dtype
        if x1_type != x2_type:
            x1_type = _handle_x64_promotion(x1_type)
            x2_type = _handle_x64_promotion(x2_type)
            promoted = _handle_x64_promotion(promote_types_jax(x1_type, x2_type))
            x1 = ivy.asarray(x1, dtype=promoted)
            x2 = ivy.asarray(x2, dtype=promoted)
    return x1, x2


from . import fft
from . import linalg
from . import creation
from .creation import *
from .dtype import can_cast, promote_types
from .scalars import *
from . import indexing
from .indexing import *
from . import logic
from .logic import *
from . import manipulations
from .manipulations import *
from . import mathematical_functions
from .mathematical_functions import *
from . import statistical
from .statistical import *
from . import searching_sorting
from .searching_sorting import *

_frontend_array = array
