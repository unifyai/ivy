import torch

valid_devices = ("cpu", "gpu")
invalid_devices = ("tpu",)

valid_dtypes = [
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "bfloat16",
    "float16",
    "float32",
    "float64",
    "complex64",
    "complex128",
    "bool",
]
invalid_dtypes = [
    "uint16",
    "uint32",
    "uint64",
]

valid_numeric_dtypes = [
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "bfloat16",
    "float16",
    "float32",
    "float64",
    "complex64",
    "complex128",
]
invalid_numeric_dtypes = [
    "uint16",
    "uint32",
    "uint64",
]

valid_int_dtypes = [
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
]
invalid_int_dtypes = [
    "uint16",
    "uint32",
    "uint64",
]

valid_uint_dtypes = [
    "uint8",
]
invalid_uint_dtypes = [
    "uint16",
    "uint32",
    "uint64",
]

valid_float_dtypes = [
    "bfloat16",
    "float16",
    "float32",
    "float64",
]
invalid_float_dtypes = []

valid_complex_dtypes = [
    "complex64",
    "complex128",
]
invalid_complex_dtypes = []


# Helpers for function testing


Dtype = torch.dtype
Device = torch.device


def native_array(x):
    return torch.tensor(x)


def is_native_array(x):
    return isinstance(x, (torch.Tensor, torch.nn.Parameter))


def to_numpy(x):
    return x.numpy()


def as_native_dtype(dtype: str):
    return torch.tensor([], dtype=dtype).dtype


def as_native_dev(device: str):
    return torch.device(device)


def isscalar(x):
    return x.dim() == 0
