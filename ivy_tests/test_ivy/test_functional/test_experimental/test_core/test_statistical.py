# global
from hypothesis import strategies as st

# local
import numpy as np
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_test


# Helpers #
# ------- #


@st.composite
def statistical_dtype_values(draw, *, function):
    large_abs_safety_factor = 2
    small_abs_safety_factor = 2
    if function in ["mean", "median", "std", "var"]:
        large_abs_safety_factor = 24
        small_abs_safety_factor = 24
    dtype, values, axis = draw(
        helpers.dtype_values_axis(
            available_dtypes=helpers.get_dtypes("float"),
            large_abs_safety_factor=large_abs_safety_factor,
            small_abs_safety_factor=small_abs_safety_factor,
            safety_factor_scale="log",
            min_num_dims=1,
            max_num_dims=5,
            min_dim_size=2,
            valid_axis=True,
            allow_neg_axes=False,
            min_axes_size=1,
        )
    )
    shape = values[0].shape
    size = values[0].size
    max_correction = np.min(shape)
    if function == "var" or function == "std":
        if size == 1:
            correction = 0
        elif isinstance(axis, int):
            correction = draw(
                helpers.ints(min_value=0, max_value=shape[axis] - 1)
                | helpers.floats(min_value=0, max_value=shape[axis] - 1)
            )
            return dtype, values, axis, correction
        else:
            correction = draw(
                helpers.ints(min_value=0, max_value=max_correction - 1)
                | helpers.floats(min_value=0, max_value=max_correction - 1)
            )
        return dtype, values, axis, correction
    return dtype, values, axis


#TODO: helpers.get_dtypes(kind="float") not working.
@st.composite
def _statistical_dtype_xs_bins_range_axis_castable(draw, n:int=2):
    available_dtypes = draw(helpers.get_dtypes(kind="float"))
    shape = draw(helpers.get_shape(min_num_dims=1))
    dtype, values = draw(
        helpers.dtype_and_values(
            available_dtypes=available_dtypes,
            num_arrays=n,
            shared_dtype=True,
            shape=shape,
        )
    )
    axis = draw(helpers.get_axis(shape=shape, force_int=True))
    dtype1, values, dtype2 = draw(
        helpers.get_castable_dtype(draw(available_dtypes), dtype[0], values[:n])
    )
    bins = draw(
        helpers.array_values(
            dtype=dtype1,
            shape=(helpers.ints(),),
        )
        |
        helpers.ints()
    )
    range = ()
    if isinstance(bins, int):
        range = (draw(helpers.floats()), draw(helpers.floats()))
    else:
        bins = sorted(bins)
        range = None
    return dtype1, values, bins, range, axis, dtype2


#TODO: check after solving _statistical_dtype_xs_bins_range_axis_castable.
@handle_test(
    fn_tree="functional.experimental.histogram",
    statistical_dtype_xs_bins_range_axis_castable=_statistical_dtype_xs_bins_range_axis_castable(),
    extend_lower_interval=st.booleans(),
    extend_upper_interval=st.booleans(),
    density=st.booleans(),
)
def test_histogram(
    *,
    statistical_dtype_xs_bins_range_axis_castable,
    extend_lower_interval,
    extend_upper_interval,
    density,
    as_variable,
    num_positional_args,
    native_array,
    container_flags,
    with_out,
    instance_method,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    input_dtype, values, bins, range, axis, castable = statistical_dtype_xs_bins_range_axis_castable
    helpers.test_function(
        a=values[0],
        bins=bins,
        axis=axis,
        extend_lower_interval=extend_lower_interval,
        extend_upper_interval=extend_upper_interval,
        dtype=castable,
        range=range,
        weights=values[1],
        density=density,
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container_flags,
        with_out=with_out,
        instance_method=instance_method,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        ground_truth_backend=ground_truth_backend,
    )


@handle_test(
    fn_tree="functional.experimental.median",
    dtype_x_axis=statistical_dtype_values(function="median"),
    keep_dims=st.booleans(),
)
def test_median(
    *,
    dtype_x_axis,
    keep_dims,
    num_positional_args,
    as_variable,
    with_out,
    native_array,
    container_flags,
    instance_method,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=input_dtype,
        num_positional_args=num_positional_args,
        as_variable_flags=as_variable,
        with_out=with_out,
        native_array_flags=native_array,
        container_flags=container_flags,
        instance_method=instance_method,
        on_device=on_device,
        fw=backend_fw,
        fn_name=fn_name,
        input=x[0],
        axis=axis,
        keepdims=keep_dims,
    )


# nanmean
@handle_test(
    fn_tree="functional.experimental.nanmean",
    dtype_x_axis=statistical_dtype_values(function="nanmean"),
    keep_dims=st.booleans(),
    dtype=helpers.get_dtypes("float"),
)
def test_nanmean(
    *,
    dtype_x_axis,
    keep_dims,
    dtype,
    num_positional_args,
    as_variable,
    with_out,
    native_array,
    container_flags,
    instance_method,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container_flags,
        instance_method=instance_method,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        a=x[0],
        axis=axis,
        keepdims=keep_dims,
        dtype=dtype,
    )


# unravel_index
@st.composite
def max_value_as_shape_prod(draw):
    shape = draw(
        helpers.get_shape(
            min_num_dims=1,
            max_num_dims=5,
            min_dim_size=1,
            max_dim_size=5,
        )
    )
    dtype_and_x = draw(
        helpers.dtype_values_axis(
            available_dtypes=helpers.get_dtypes("integer"),
            min_value=0,
            max_value=np.prod(shape) - 1,
        )
    )
    return dtype_and_x, shape


@handle_test(
    fn_tree="functional.experimental.nanmean",
    dtype_x_shape=max_value_as_shape_prod(),
)
def test_unravel_index(
    dtype_x_shape,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    backend_fw,
    fn_name,
    ground_truth_backend,
):
    dtype_and_x, shape = dtype_x_shape
    input_dtype, x = dtype_and_x[0], dtype_and_x[1]
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container,
        instance_method=instance_method,
        fw=backend_fw,
        fn_name=fn_name,
        indices=np.asarray(x[0], dtype=input_dtype[0]),
        shape=shape,
    )
