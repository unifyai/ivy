# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy.functional.backends.numpy as ivy_np
import ivy_tests.test_ivy.helpers as helpers


# cross_entropy
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtypes, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=helpers.num_positional_args(fn_name="cross_entropy"),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_cross_entropy(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    input_dtype, x = dtype_and_x
    if (v == [] for v in x):
        return
    if fw == "torch" and input_dtype == "float16":
        return
    helpers.test_array_function(
        input_dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "cross_entropy",
        true=np.asarray(x[0], dtype=input_dtype[0]),
        pred=np.asarray(x[1], dtype=input_dtype[1]),
    )


# binary_cross_entropy
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtypes, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=helpers.num_positional_args(fn_name="binary_cross_entropy"),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_binary_cross_entropy(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    input_dtype, x = dtype_and_x
    if (v == [] for v in x):
        return
    if fw == "torch" and input_dtype == "float16":
        return
    helpers.test_array_function(
        input_dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "binary_cross_entropy",
        true=np.asarray(x[0], dtype=input_dtype[0]),
        pred=np.asarray(x[1], dtype=input_dtype[1]),
    )


# sparse_cross_entropy
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtypes, 2),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    with_out=st.booleans(),
    num_positional_args=helpers.num_positional_args(fn_name="sparse_cross_entropy"),
    native_array=helpers.list_of_length(st.booleans(), 2),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
)
def test_sparse_cross_entropy(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    input_dtype, x = dtype_and_x
    if (v == [] for v in x):
        return
    if fw == "torch" and input_dtype == "float16":
        return
    helpers.test_array_function(
        input_dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "sparse_cross_entropy",
        true=np.asarray(x[0], dtype=input_dtype[0]),
        pred=np.asarray(x[1], dtype=input_dtype[1]),
    )
