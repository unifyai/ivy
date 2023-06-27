# global
from hypothesis import strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test
from ivy_tests.test_ivy.test_functional.test_core.test_statistical import (
    _statistical_dtype_values,
)


# mean
@handle_frontend_test(
    fn_tree="paddle.mean",
    dtype_and_x=_statistical_dtype_values(function="mean"),
    keepdim=st.booleans(),
    test_with_out=st.just(True),
)
def test_paddle_mean(
    *,
    dtype_and_x,
    keepdim,
    on_device,
    fn_tree,
    frontend,
    test_flags,
):
    input_dtype, x, axis = dtype_and_x
    test_flags.num_positional_args = len(dtype_and_x) - 2
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        axis=axis,
        keepdim=keepdim,
    )


# numel
@handle_frontend_test(
    fn_tree="paddle.numel",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
    ),
)
def test_paddle_numel(
    *,
    dtype_and_x,
    on_device,
    fn_tree,
    frontend,
    test_flags,
):
    input_dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        x=x[0],
    )

# median
@handle_frontend_test(
    fn_tree="paddle.median",
    dtype_and_x=_statistical_dtype_values(function="median"),
    keepdim=st.booleans(),
)

def test_paddle_median(
    *,
    dtype_and_x,
    keep_dims,
    test_flags,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    input_dtype, x, axis = dtype_and_x
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=input_dtype,
        test_flags=test_flags,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        rtol_=1e-1,
        atol_=1e-1,
        x=x[0],
        axis=axis,
        keepdims=keep_dims,
    )