# global

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


# selu
@handle_frontend_test(
    fn_tree="paddle.nn.functional.selu",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        safety_factor_scale="log",
        small_abs_safety_factor=20,
    ),
    scale=helpers.ints(min_value=2, max_value=10),
    alpha=helpers.ints(min_value=1, max_value=10),
)
def test_paddle_selu(
    *,
    dtype_and_x,
    scale,
    alpha,
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
        alpha=alpha,
        scale=scale,
    )


# hardshrink
@handle_frontend_test(
    fn_tree="paddle.nn.functional.hardshrink",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
    ),
    threshold=helpers.floats(min_value=0, max_value=1, exclude_min=True),
)
def test_paddle_hardshrink(
    *,
    dtype_and_x,
    threshold,
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
        threshold=threshold,
    )


# hardsigmoid
@handle_frontend_test(
    fn_tree="paddle.nn.functional.hardsigmoid",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
    ),
    slope=helpers.ints(min_value=0, max_value=10),
    offset=helpers.ints(min_value=0, max_value=10),
)
def test_paddle_hardsigmoid(
    *,
    dtype_and_x,
    slope,
    offset,
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
        slope=slope,
        offset=offset,
    )
