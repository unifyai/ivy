"""Collection of tests for elementwise functions."""

# global
import numpy as np
from hypothesis import given, assume, strategies as st
from numbers import Number

# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.numpy as ivy_np


# abs
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_abs(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "abs",
        x=np.asarray(x, dtype=dtype),
    )


# acosh
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_acosh(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "acosh",
        x=np.asarray(x, dtype=dtype),
    )


# acos
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_acos(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "acos",
        x=np.asarray(x, dtype=dtype),
    )


# add
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_add(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if any([d == "float16" for d in dtype]):
        return  # numpy array api doesnt support float16
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "add",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# asin
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_asin(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "asin",
        x=np.asarray(x, dtype=dtype),
    )


# asinh
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_asinh(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "asinh",
        x=np.asarray(x, dtype=dtype),
    )


# atan
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_atan(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "atan",
        x=np.asarray(x, dtype=dtype),
    )


# atan2
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_atan2(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and "float16" in dtype:
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "atan2",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# atanh
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_atanh(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "atanh",
        x=np.asarray(x, dtype=dtype),
    )


# bitwise_and
@given(
    dtype_and_x=helpers.dtype_and_values(ivy.int_dtype_strs + ("bool",), 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_bitwise_and(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "bitwise_and",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# bitwise_left_shift
@given(
    dtype_and_x=helpers.dtype_and_values(ivy.int_dtype_strs),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_bitwise_left_shift(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    assume(x)
    x1 = np.asarray(x, dtype=dtype)
    n_bits = ivy.dtype_bits(dtype)
    x2 = np.random.randint(n_bits, size=x1.shape, dtype=dtype)
    helpers.test_array_function(
        [dtype, dtype],
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "bitwise_left_shift",
        x1=x1,
        x2=x2,
    )


# bitwise_invert
@given(
    dtype_and_x=helpers.dtype_and_values(ivy.int_dtype_strs + ("bool",)),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_bitwise_invert(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "bitwise_invert",
        x=np.asarray(x, dtype=dtype),
    )


# bitwise_or
@given(
    dtype_and_x=helpers.dtype_and_values(ivy.int_dtype_strs + ("bool",), 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_bitwise_or(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "bitwise_or",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# bitwise_right_shift
@given(
    dtype_and_x=helpers.dtype_and_values(ivy.int_dtype_strs),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_bitwise_right_shift(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    assume(x)
    x1 = np.asarray(x, dtype=dtype)
    n_bits = ivy.dtype_bits(dtype)
    x2 = np.random.randint(n_bits, size=x1.shape, dtype=dtype)
    helpers.test_array_function(
        [dtype, dtype],
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "bitwise_right_shift",
        x1=x1,
        x2=x2,
    )


# bitwise_xor
@given(
    dtype_and_x=helpers.dtype_and_values(ivy.int_dtype_strs + ("bool",), 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_bitwise_xor(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "bitwise_xor",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# ceil
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_ceil(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "ceil",
        x=np.asarray(x, dtype=dtype),
    )


# cos
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_cos(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "cos",
        x=np.asarray(x, dtype=dtype),
    )


# cosh
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_cosh(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "cosh",
        x=np.asarray(x, dtype=dtype),
    )


# divide
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_divide(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if any(xi == 0 for xi in x[1]):
        return  # don't divide by 0
    if any(
        xi > 9223372036854775807 or yi > 9223372036854775807
        for xi, yi in zip(x[0], x[1])
    ):
        return  # np.divide converts to signed int so values can't be too large
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "divide",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# equal
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_equal(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "equal",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# exp
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_exp(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "exp",
        x=np.asarray(x, dtype=dtype),
    )


# expm1
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_expm1(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "expm1",
        x=np.asarray(x, dtype=dtype),
    )


# floor
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_floor(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "floor",
        x=np.asarray(x, dtype=dtype),
    )


# floor_divide - don't allow inf as array API spec allows varying behaviour
# for special cases
@given(
    dtype_and_x=helpers.dtype_and_values(
        ivy_np.valid_numeric_dtype_strs, n_arrays=2, allow_inf=False
    ),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_floor_divide(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    assume(0 not in x[1])
    if fw == "tensorflow":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "floor_divide",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# greater
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_greater(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "greater",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# greater_equal
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_greater_equal(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "greater_equal",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# isfinite
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_isfinite(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "isfinite",
        x=np.asarray(x, dtype=dtype),
    )


# isinf
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_isinf(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "isinf",
        x=np.asarray(x, dtype=dtype),
    )


# isnan
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_isnan(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "isnan",
        x=np.asarray(x, dtype=dtype),
    )


# less
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_less(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "less",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# less_equal
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_less_equal(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "less_equal",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# log
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_log(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "log",
        x=np.asarray(x, dtype=dtype),
    )


# log1p
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_log1p(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "log1p",
        x=np.asarray(x, dtype=dtype),
    )


# log2
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_log2(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "log2",
        x=np.asarray(x, dtype=dtype),
    )


# log10
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_log10(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "log10",
        x=np.asarray(x, dtype=dtype),
    )


# logaddexp
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_logaddexp(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and "float16" in dtype:
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "logaddexp",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# logical_and
@given(
    dtype_and_x=helpers.dtype_and_values(("bool",), 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_logical_and(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "logical_and",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# logical_not
@given(
    dtype_and_x=helpers.dtype_and_values(("bool",)),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_logical_not(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "logical_not",
        x=np.asarray(x, dtype=dtype),
    )


# logical_or
@given(
    dtype_and_x=helpers.dtype_and_values(("bool",), 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_logical_or(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "logical_or",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# logical_xor
@given(
    dtype_and_x=helpers.dtype_and_values(("bool",), 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_logical_xor(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "logical_xor",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# multiply
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_multiply(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "multiply",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# negative
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_negative(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if "uint" in dtype:
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "negative",
        x=np.asarray(x, dtype=dtype),
    )


# not_equal
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_not_equal(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "not_equal",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# positive
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_positive(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "positive",
        x=np.asarray(x, dtype=dtype),
    )


# pow
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_pow(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "jax":
        return
    if fw == "tensorflow" and any(["uint" in d for d in dtype]):
        return
    if (
        any(xi < 0 for xi in x[1])
        and ivy.is_int_dtype(dtype[1])
        and ivy.is_int_dtype(dtype[0])
    ):
        return  # ints to negative int powers not allowed
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "pow",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# remainder
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_remainder(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    assume(not any(xi == 0 for xi in x[1]))
    helpers.test_array_function(
        dtype,
        [as_variable, False],  # torch remainder not differentiable wrt to x2
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "remainder",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# round
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_round(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "round",
        x=np.asarray(x, dtype=dtype),
    )


# sign
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_sign(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "sign",
        x=np.asarray(x, dtype=dtype),
    )


# sin
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_sin(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "sin",
        x=np.asarray(x, dtype=dtype),
    )


# sinh
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_sinh(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "sinh",
        x=np.asarray(x, dtype=dtype),
    )


# square
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_square(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "square",
        x=np.asarray(x, dtype=dtype),
    )


# sqrt
@given(
    dtype_and_x=helpers.dtype_and_values(
        ivy_np.valid_float_dtype_strs, allow_inf=False
    ),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_sqrt(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "sqrt",
        x=np.asarray(x, dtype=dtype),
    )


# subtract
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 2),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_subtract(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "subtract",
        x1=np.asarray(x[0], dtype=dtype[0]),
        x2=np.asarray(x[1], dtype=dtype[1]),
    )


# tan
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_tan(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "tan",
        x=np.asarray(x, dtype=dtype),
    )


# tanh
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_tanh(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "tanh",
        x=np.asarray(x, dtype=dtype),
    )


# trunc
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_trunc(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "trunc",
        x=np.asarray(x, dtype=dtype),
    )


# Extra #
# ------#


# erf
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtype_strs),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 1),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_erf(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    if fw == "torch" and dtype == "float16":
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "erf",
        x=np.asarray(x, dtype=dtype),
    )


# minimum
@given(
    xy=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, n_arrays=2),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(1, 2),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_minimum(
    xy,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    device,
    call,
    fw,
):
    # smoke test
    dtype = xy[0]
    x = xy[1][0]
    y = xy[1][1]
    if (
        (isinstance(xy[1][0], Number) or isinstance(xy[1], Number))
        and as_variable is True
        and fw == "mxnet"
    ):
        # mxnet does not support 0-dimensional variables
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "minimum",
        x1=np.asarray(x, dtype=dtype[0]),
        x2=ivy.array(y, dtype=dtype[1]),
    )


# maximum
@given(
    xy=helpers.dtype_and_values(ivy_np.valid_numeric_dtype_strs, n_arrays=2),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(1, 2),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_maximum(
    xy,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    device,
    call,
    fw,
):
    # smoke test
    dtype = xy[0]
    x = xy[1][0]
    y = xy[1][1]
    if (
        (isinstance(xy[1][0], Number) or isinstance(xy[1], Number))
        and as_variable is True
        and fw == "mxnet"
    ):
        # mxnet does not support 0-dimensional variables
        return
    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "maximum",
        x1=np.asarray(x, dtype=dtype[0]),
        x2=ivy.array(y, dtype=dtype[1]),
    )
