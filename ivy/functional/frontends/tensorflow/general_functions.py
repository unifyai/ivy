# global
from builtins import slice as py_slice
import sys

# local
import ivy
from ivy.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from ivy.functional.frontends.tensorflow.func_wrapper import (
    to_ivy_arrays_and_back,
    handle_tf_dtype,
    to_ivy_dtype,
)
from ivy.functional.frontends.tensorflow.tensor import EagerTensor
import ivy.functional.frontends.tensorflow as tf_frontend


@to_ivy_arrays_and_back
def argsort(values, axis=-1, direction="ASCENDING", stable=False, name=None):
    if direction == "DESCENDING":
        descending = True
    else:
        descending = False
    return ivy.argsort(values, axis=axis, descending=descending, stable=stable).astype(
        "int32"
    )


@to_ivy_arrays_and_back
def clip_by_value(t, clip_value_min, clip_value_max):
    ivy.utils.assertions.check_all_or_any_fn(
        clip_value_min,
        clip_value_max,
        fn=ivy.exists,
        type="all",
        message="clip_value_min and clip_value_max must exist",
    )
    t = ivy.array(t)
    return ivy.clip(t, clip_value_min, clip_value_max)


@with_supported_dtypes({"2.9.1 and below": ("float32",)}, "tensorflow")
@to_ivy_arrays_and_back
def clip_by_global_norm(t_list, clip_norm, use_norm=None):
    if use_norm is not None:
        global_norm = use_norm
    else:
        global_norm = ivy.sqrt(ivy.sum([ivy.vector_norm(t) ** 2 for t in t_list]))

    max_clip_ratio = ivy.maximum(clip_norm, global_norm)
    return [
        ivy.multiply(t, ivy.divide(clip_norm, max_clip_ratio)) for t in t_list
    ], global_norm


@to_ivy_arrays_and_back
def clip_by_norm(t, clip_norm, axes=None):
    t = ivy.array(t)
    l2sum = ivy.sum(t * t, axis=axes, keepdims=True)
    pred = l2sum > 0

    l2sum_safe = ivy.where(pred, l2sum, ivy.ones_like(l2sum))
    l2norm = ivy.where(pred, ivy.sqrt(l2sum_safe), l2sum)
    intermediate = t * clip_norm
    assert t.shape == intermediate.shape, "Dimensions %s and %s are not compatible" % (
        t.shape,
        intermediate.shape,
    )
    t_clip = intermediate / ivy.maximum(l2norm, clip_norm)
    return t_clip


@with_unsupported_dtypes({"2.9.0 and below": ("float16", "bfloat16")}, "tensorflow")
@handle_tf_dtype
@to_ivy_arrays_and_back
def eye(num_rows, num_columns=None, batch_shape=None, dtype=ivy.float32, name=None):
    return ivy.eye(num_rows, num_columns, batch_shape=batch_shape, dtype=dtype)


@to_ivy_arrays_and_back
def fill(dims, value, name=None):
    return ivy.full(dims, value)


@with_unsupported_dtypes({"2.9.0 and below": ("float16", "bfloat16")}, "tensorflow")
@handle_tf_dtype
@to_ivy_arrays_and_back
def ones(shape, dtype=ivy.float32, name=None):
    return ivy.ones(shape, dtype=dtype)


@handle_tf_dtype
@to_ivy_arrays_and_back
def zeros_like(input, dtype=None, name=None):
    return ivy.zeros_like(input, dtype=dtype)


@handle_tf_dtype
def constant(value, dtype=None, shape=None, name=None):
    if shape is not None:
        value = ivy.reshape(value, shape=shape)
    if dtype is not None:
        return EagerTensor(ivy.astype(value, dtype))
    return EagerTensor(value)


@handle_tf_dtype
def convert_to_tensor(value, dtype=None, dtype_hint=None, name=None):
    if dtype:
        return tf_frontend.cast(value, dtype)
    elif dtype_hint:
        return tf_frontend.cast(value, dtype_hint)
    if hasattr(value, "ivy_array"):
        return EagerTensor(value.ivy_array)
    return EagerTensor(value)


@to_ivy_arrays_and_back
def einsum(equation, *inputs, **kwargs):
    return ivy.einsum(equation, *inputs)


@to_ivy_arrays_and_back
def reshape(tensor, shape, name=None):
    shape = shape.to_list() if ivy.is_array(shape) else shape
    return ivy.reshape(tensor, shape=shape)


@to_ivy_arrays_and_back
def rank(input, **kwargs):
    return ivy.astype(ivy.array(input.ndim), ivy.int32)


@handle_tf_dtype
@to_ivy_arrays_and_back
def ones_like(input, dtype=None, name=None):
    return ivy.ones_like(input, dtype=dtype)


@handle_tf_dtype
@to_ivy_arrays_and_back
def zeros(shape, dtype=ivy.float32, name=None):
    return ivy.zeros(shape=shape, dtype=dtype)


@to_ivy_arrays_and_back
def expand_dims(input, axis, name=None):
    return ivy.expand_dims(input, axis=axis)


@to_ivy_arrays_and_back
def squeeze(input, axis=None, name=None):
    return ivy.squeeze(input, axis=axis)


@to_ivy_arrays_and_back
def concat(values, axis, name=None):
    return ivy.concat(values, axis=axis)


@to_ivy_arrays_and_back
def shape(input, out_type=ivy.int32, name=None):
    out_type = to_ivy_dtype(out_type)
    if out_type in ["int32", "int64"]:
        return ivy.array(ivy.shape(input), dtype=out_type)
    else:
        return ivy.array(ivy.shape(input), dtype="int64")


@to_ivy_arrays_and_back
def shape_n(input, out_type=ivy.int32, name=None):
    out_type = to_ivy_dtype(out_type)
    if out_type in ["int32", "int64"]:
        return [ivy.array(ivy.shape(i), dtype=out_type) for i in input]
    else:
        return [ivy.array(ivy.shape(i), dtype="int64") for i in input]


@to_ivy_arrays_and_back
def size(input, out_type=ivy.int32, name=None):
    out_type = to_ivy_dtype(out_type)
    shape = ivy.shape(input, as_array=True)
    return ivy.astype(ivy.prod(shape), out_type, copy=False)


@to_ivy_arrays_and_back
def ensure_shape(x, shape, name=None):
    x = EagerTensor(x)
    x.set_shape(shape)

    return x


@with_unsupported_dtypes({"2.10.0 and below": ("float16", "bfloat16")}, "tensorflow")
@handle_tf_dtype
@to_ivy_arrays_and_back
def range(start, limit=None, delta=1, /, *, dtype=None, name=None):
    return ivy.arange(start, limit, delta, dtype=dtype)


@to_ivy_arrays_and_back
def sort(values, axis=-1, direction="ASCENDING", name=None):
    descending = True
    if direction == "ASCENDING":
        descending = False
    else:
        ivy.utils.assertions.check_equal(
            direction,
            "DESCENDING",
            message="Argument `direction` should be one of 'ASCENDING' or 'DESCENDING'",
        )
    return ivy.sort(values, axis=axis, descending=descending)


@to_ivy_arrays_and_back
def searchsorted(sorted_sequence, values, side="left", out_type="int32"):
    out_type = to_ivy_dtype(out_type)
    if out_type not in ["int32", "int64"]:
        out_type = "int64"
    return ivy.searchsorted(sorted_sequence, values, side=side, ret_dtype=out_type)


@to_ivy_arrays_and_back
def identity(input, name=None):
    return ivy.copy_array(input)


def stack(values, axis=0, name="stack"):
    return ivy.stack(values, axis=axis)


@to_ivy_arrays_and_back
def is_tensor(x, name=None):
    return ivy.is_array(x)


@to_ivy_arrays_and_back
def gather(params, indices, axis=None, batch_dims=0, name=None):
    return ivy.gather(params, indices, axis=axis, batch_dims=batch_dims)


@to_ivy_arrays_and_back
def gather_nd(params, indices, batch_dims=0, name=None):
    return ivy.gather_nd(params, indices, batch_dims=batch_dims)


@to_ivy_arrays_and_back
def boolean_mask(tensor, mask, axis=None, name=None):
    if axis is None or axis == 0:
        return ivy.get_item(tensor, mask)
    else:
        n = ivy.get_num_dims(tensor)
        k = ivy.get_num_dims(mask)
        if axis < 0:
            axis = n + axis
        ivy.utils.assertions.check_less(
            k + axis,
            n,
            allow_equal=True,
            message="Value of axis must be \
                                           such that axis + dim(mask) <= dim(tensor)",
        )
        tensor_shape = ivy.shape(tensor)
        for i in range(axis - 1, -1, -1):
            mask = ivy.expand_dims(mask, axis=0)
            mask = ivy.repeat(mask, tensor_shape[i], axis=0)
        return ivy.get_item(tensor, mask)


@to_ivy_arrays_and_back
def pad(tensor, paddings, mode="CONSTANT", constant_values=0, name=None):
    paddings = paddings.to_list() if ivy.is_array(paddings) else paddings
    return ivy.pad(tensor, paddings, mode=mode.lower(), constant_values=constant_values)


@to_ivy_arrays_and_back
def transpose(a, perm=None, conjugate=False, name="transpose"):
    # handle conjugate when ivy supports complex numbers
    if perm is not None:
        return ivy.permute_dims(a, axes=perm)
    n = a.ndim
    perm = ivy.arange(n - 1, -1, -1)
    return ivy.permute_dims(a, axes=perm)


def _num_to_bit_list(value, num_dims):
    return list(map(int, "{:0{size}b}".format(value, size=num_dims)))[::-1]


# ToDo: find a way around for negative indexing, which torch does not support
@to_ivy_arrays_and_back
def strided_slice(
    input_,
    begin,
    end,
    strides=None,
    begin_mask=0,
    end_mask=0,
    ellipsis_mask=0,
    new_axis_mask=0,
    shrink_axis_mask=0,
    var=None,
    name=None,
):
    input_shape = list(input_.shape)
    input_rank = len(input_shape)
    begin_mask, end_mask, ellipsis_mask, new_axis_mask, shrink_axis_mask = list(
        map(
            _num_to_bit_list,
            [begin_mask, end_mask, ellipsis_mask, new_axis_mask, shrink_axis_mask],
            [input_rank] * 5,
        )
    )
    begin, end, strides = map(
        lambda x: ivy.array(x) if isinstance(x, int) else x, [begin, end, strides]
    )
    num_defined = len(begin)
    strides = ivy.repeat(ivy.array(1), num_defined) if strides is None else strides
    ivy.assertions.check_true(
        num_defined == len(end) == len(strides),
        message="`begin`, `end`, and `strides` are expected to have the same length",
    )
    begin, end, strides = map(
        lambda x: [ivy.to_scalar(i) for i in x] if ivy.is_ivy_array(x) else x,
        [begin, end, strides],
    )
    for i, v in enumerate(shrink_axis_mask):
        if v == 1:
            begin_mask[i] = 0
    ellipsis_indices = [i for i, v in enumerate(ellipsis_mask) if v]
    if len(ellipsis_indices) > 1:
        raise ValueError("Multiple ellipses are not allowed.")
    elif len(ellipsis_indices) == 1:
        ellipsis_index = ellipsis_indices[0]
        num_missing = input_rank - len(begin)
        if num_missing == 0:
            begin_mask[ellipsis_index] = 1
            end_mask[ellipsis_index] = 1
            shrink_axis_mask[ellipsis_index] = 0
            new_axis_mask[ellipsis_index] = 0
        else:
            for i in py_range(ellipsis_index, ellipsis_index + num_missing + 1, 1):
                if i < input_rank:
                    shrink_axis_mask[i] = 0
                    new_axis_mask[i] = 0
                else:
                    break
            if ellipsis_index >= len(begin):
                begin = begin + [None] * num_missing
                end = end + [None] * num_missing
                strides = strides + [1] * num_missing
            else:
                begin = (
                    begin[:ellipsis_index]
                    + [None] * (num_missing + 1)
                    + begin[ellipsis_index + 1 :]
                )
                end = (
                    end[:ellipsis_index]
                    + [None] * (num_missing + 1)
                    + end[ellipsis_index + 1 :]
                )
                strides = (
                    strides[:ellipsis_index]
                    + [1] * (num_missing + 1)
                    + strides[ellipsis_index + 1 :]
                )
    full_slice = ()
    for i, _ in enumerate(begin):
        if new_axis_mask[i]:
            full_slice += (ivy.newaxis,)
        else:
            b = begin[i] if not begin_mask[i] else None
            e = end[i] if not end_mask[i] else None
            s = strides[i]
            if b is None and e is None:
                s = 1 if ellipsis_mask[i] else s
            elif shrink_axis_mask[i]:
                if b is not None:
                    e = b + 1 if s > 0 else b - 1
                else:
                    e = 1 if s > 0 else input_shape[i] - 2
            full_slice += (py_slice(b, e, s),)
    if all(i is None for i in full_slice):
        full_slice += (...,)
    ret = input_[full_slice]
    shrink_indices = [
        i
        for i, v in enumerate(shrink_axis_mask)
        if v and i < len(ret.shape) and ret.shape[i] == 1
    ]
    ret = ivy.squeeze(ret, axis=shrink_indices)
    return ret


@to_ivy_arrays_and_back
def slice(input_, begin, size, name=None):
    return strided_slice(input_, begin, begin + size)


@to_ivy_arrays_and_back
def linspace(start, stop, num, name=None, axis=0):
    return ivy.linspace(start, stop, num, axis=axis)


@to_ivy_arrays_and_back
def realdiv(x, y, name=None):
    return ivy.divide(x, y)


@with_unsupported_dtypes({"2.9.0 and below": ("uint16",)}, "tensorflow")
@to_ivy_arrays_and_back
def tile(input, multiples, name=None):
    return ivy.tile(input, multiples)


@to_ivy_arrays_and_back
def one_hot(
    indices: ivy.Array,
    depth: int,
    on_value=None,
    off_value=None,
    axis=None,
    dtype=None,
    device=None,
    out=None,
):
    return ivy.one_hot(indices, depth)


@to_ivy_arrays_and_back
def where(condition: ivy.Array, x=None, y=None, name=None):
    if x is None and y is None:
        return ivy.argwhere(condition)
    else:
        return ivy.where(condition, x, y)


def roll(input, shift, axis, name=None):
    return ivy.roll(input, shift, axis=axis)


@to_ivy_arrays_and_back
def unique_with_counts(x, return_counts=False, axis=None):
    """
    Return unique values and their counts from an array.

    Args:
        x (array): Input array.
        return_counts (bool, optional): If True, also return the number of
        times each unique value appears. Default is False.
        axis (int, optional): The axis along which to operate. If None,
        the entire array is used. Default is None.

    Returns:
        array: Unique values of the array.
        array (optional): The number of times each unique
        value appears in the array (if return_counts=True).
    """
    x = ivy.array(x)
    unique_vals, inverse_indices, counts = ivy.unique(
        x, return_inverse=True, return_counts=True, axis=axis)
    if return_counts:
        return unique_vals, counts
    else:
        return unique_vals

@to_ivy_arrays_and_back
def split(value, num_or_size_splits, axis=0, num=None, name=None):
    return ivy.split(
        value, num_or_size_splits=num_or_size_splits, axis=axis, with_remainder=False
    )


def repeat(
    input,
    repeats,
    axis=None,
    name=None,
):
    return ivy.repeat(input, repeats, axis=axis)


@with_unsupported_dtypes({"1.11.0 and below": ("float16", "bfloat16")}, "tensorflow")
@to_ivy_arrays_and_back
def unstack(value: ivy.Array, axis=0, num=None, name=None):
    return ivy.unstack(value, axis=axis)


@to_ivy_arrays_and_back
def reverse(tensor, axis, name=None):
    return ivy.flip(tensor, axis=axis)


@to_ivy_arrays_and_back
def norm(tensor, ord="euclidean", axis=None, keepdims=None, name=None):
    return tf_frontend.linalg.norm(
        tensor, ord=ord, axis=axis, keepdims=keepdims, name=name
    )


norm.supported_dtypes = (
    "float32",
    "float64",
)
