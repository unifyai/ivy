# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.jax as ivy_jax


# add
@given(
    dtype_and_x=helpers.dtype_and_values(
        ivy_jax.valid_float_dtypes, 2, shared_dtype=True
    ),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.jax.lax.add"
    ),
    native_array=helpers.list_of_length(st.booleans(), 2),
)
def test_jax_add(
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_function(
        input_dtype,
        as_variable,
        False,
        num_positional_args,
        native_array,
        fw,
        "jax",
        "lax.add",
        x=np.asarray(x[0], dtype=input_dtype[0]),
        y=np.asarray(x[1], dtype=input_dtype[1]),
    )


# tan
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_jax.valid_float_dtypes),
    as_variable=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.jax.lax.tan"
    ),
    native_array=st.booleans(),
)
def test_jax_tan(
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_function(
        input_dtype,
        as_variable,
        False,
        num_positional_args,
        native_array,
        fw,
        "jax",
        "lax.tan",
        x=np.asarray(x, dtype=input_dtype),
    )
