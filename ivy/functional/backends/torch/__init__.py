# global
import sys
from types import SimpleNamespace
import torch as torch

# local
import ivy

backend_version = {"version": torch.__version__.split("+")[0]}

# noinspection PyUnresolvedReferences
if not ivy.is_local():
    _module_in_memory = sys.modules[__name__]
else:
    _module_in_memory = sys.modules[ivy.import_module_path].import_cache[__name__]

use = ivy.utils.backend.ContextManager(_module_in_memory)

NativeArray = torch.Tensor
NativeVariable = torch.Tensor
NativeDevice = torch.device
NativeDtype = torch.dtype
NativeShape = torch.Size

NativeSparseArray = torch.Tensor


# devices
valid_devices = ("cpu", "gpu")

invalid_devices = ("tpu",)


# native data types
native_int8 = torch.int8
native_int16 = torch.int16
native_int32 = torch.int32
native_int64 = torch.int64
native_uint8 = torch.uint8
native_bfloat16 = torch.bfloat16
native_float16 = torch.float16
native_float32 = torch.float32
native_float64 = torch.float64
native_complex64 = torch.complex64
native_complex128 = torch.complex128
native_double = native_float64
native_bool = torch.bool

# valid data types
# ToDo: Add complex dtypes to valid_dtypes and fix all resulting failures.
valid_dtypes = (
    ivy.int8,
    ivy.int16,
    ivy.int32,
    ivy.int64,
    ivy.uint8,
    ivy.bfloat16,
    ivy.float16,
    ivy.float32,
    ivy.float64,
    ivy.complex64,
    ivy.complex128,
    ivy.bool,
)
valid_numeric_dtypes = (
    ivy.int8,
    ivy.int16,
    ivy.int32,
    ivy.int64,
    ivy.uint8,
    ivy.bfloat16,
    ivy.float16,
    ivy.float32,
    ivy.float64,
)
valid_int_dtypes = (ivy.int8, ivy.int16, ivy.int32, ivy.int64, ivy.uint8)
valid_float_dtypes = (ivy.bfloat16, ivy.float16, ivy.float32, ivy.float64)
valid_uint_dtypes = (ivy.uint8,)
valid_complex_dtypes = (ivy.complex64, ivy.complex128)

# invalid data types
invalid_dtypes = (
    ivy.uint16,
    ivy.uint32,
    ivy.uint64,
)
invalid_numeric_dtypes = (ivy.uint16, ivy.uint32, ivy.uint64)
invalid_int_dtypes = (ivy.uint16, ivy.uint32, ivy.uint64)
invalid_float_dtypes = ()
invalid_uint_dtypes = (ivy.uint16, ivy.uint32, ivy.uint64)
invalid_complex_dtypes = ()

native_inplace_support = True

supports_gradients = True


def closest_valid_dtype(type=None, /, as_native=False):
    if type is None:
        type = ivy.default_dtype()
    elif isinstance(type, str) and type in invalid_dtypes:
        type = ivy.as_ivy_dtype(
            {"uint16": ivy.uint8, "uint32": ivy.uint8, "uint64": ivy.uint8}[type]
        )
    return ivy.as_ivy_dtype(type) if not as_native else ivy.as_native_dtype(type)


backend = "torch"

# local sub-modules
from . import activations
from .activations import *
from . import creation
from .creation import *
from . import data_type
from .data_type import *
from . import device
from .device import *
from . import elementwise
from .elementwise import *
from . import gradients
from .gradients import *
from . import general
from .general import *
from . import layers
from .layers import *
from . import linear_algebra as linalg
from .linear_algebra import *
from . import manipulation
from .manipulation import *
from . import random
from .random import *
from . import searching
from .searching import *
from . import set
from .set import *
from . import sorting
from .sorting import *
from . import statistical
from .statistical import *
from . import utility
from .utility import *
from . import experimental
from .experimental import *
from . import control_flow_ops
from .control_flow_ops import *


# sub-backends
try:
    from . import sub_backends
    from .sub_backends import *

except ImportError:
    sub_backends = SimpleNamespace()
    available_sub_backends = []
    sub_backends_attrs = []