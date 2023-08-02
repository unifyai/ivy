# global
import numpy as np
from hypothesis import strategies as st, assume

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy_tests.test_ivy.test_frontends.test_numpy.helpers as np_frontend_helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


# helpers
@st.composite
def _get_castable_dtypes_values(draw, *, allow_nan=False, use_where=False):
    available_dtypes = helpers.get_dtypes("numeric")
    shape = draw(helpers.get_shape(min_num_dims=1, max_num_dims=4, max_dim_size=6))
    dtype, values = draw(
        helpers.dtype_and_values(
            available_dtypes=available_dtypes,
            num_arrays=1,
            large_abs_safety_factor=24,
            small_abs_safety_factor=24,
            safety_factor_scale="log",
            shape=shape,
            allow_nan=allow_nan,
        )
    )
    axis = draw(helpers.get_axis(shape=shape, force_int=True))
    dtype1, values, dtype2 = draw(
        helpers.get_castable_dtype(draw(available_dtypes), dtype[0], values[0])
    )
    if use_where:
        where = draw(np_frontend_helpers.where(shape=shape))
        return [dtype1], [values], axis, dtype2, where
    return [dtype1], [values], axis, dtype2


# sum
@handle_frontend_test(
    fn_tree="numpy.sum",
    dtype_x_axis_dtype=_get_castable_dtypes_values(use_where=True),
    keep_dims=st.booleans(),
    initial=st.one_of(st.floats(min_value=-100, max_value=100)),
)
def test_numpy_sum(
    dtype_x_axis_dtype,
    keep_dims,
    initial,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
):
    input_dtypes, x, axis, dtype, where = dtype_x_axis_dtype
    if backend_fw == "torch":
        assume(not test_flags.as_variable[0])
    where, input_dtypes, test_flags = np_frontend_helpers.handle_where_and_array_bools(
        where=where,
        input_dtype=input_dtypes,
        test_flags=test_flags,
    )
    helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        x=x[0],
        axis=axis,
        dtype=dtype,
        keepdims=keep_dims,
        initial=initial,
        where=where,
    )


# prod
@handle_frontend_test(
    fn_tree="numpy.prod",
    dtype_x_axis_dtype=_get_castable_dtypes_values(use_where=True),
    keep_dims=st.booleans(),
    initial=st.one_of(st.floats(min_value=-100, max_value=100)),
)
def test_numpy_prod(
    dtype_x_axis_dtype,
    keep_dims,
    initial,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
):
    input_dtypes, x, axis, dtype, where = dtype_x_axis_dtype
    if backend_fw == "torch":
        assume(not test_flags.as_variable[0])
    where, input_dtypes, test_flags = np_frontend_helpers.handle_where_and_array_bools(
        where=where,
        input_dtype=input_dtypes,
        test_flags=test_flags,
    )
    helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        x=x[0],
        axis=axis,
        dtype=dtype,
        keepdims=keep_dims,
        initial=initial,
        where=where,
    )


# cumsum
@handle_frontend_test(
    fn_tree="numpy.cumsum",
    dtype_and_x_axis_dtype=_get_castable_dtypes_values(),
)
def test_numpy_cumsum(
    dtype_and_x_axis_dtype,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
):
    input_dtypes, x, axis, dtype = dtype_and_x_axis_dtype
    # ToDo: set as_variable_flags as the parameter generated by test_cumprod once
    # this issue is marked as completed https://github.com/pytorch/pytorch/issues/75733
    if backend_fw == "torch":
        assume(not test_flags.as_variable[0])
    np_frontend_helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        x=x[0],
        axis=axis,
        dtype=dtype,
    )


# cumprod
@handle_frontend_test(
    fn_tree="numpy.cumprod",
    dtype_x_axis_dtypes=_get_castable_dtypes_values(),
)
def test_numpy_cumprod(
    dtype_x_axis_dtypes,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
):
    input_dtypes, x, axis, dtype = dtype_x_axis_dtypes
    # ToDo: set as_variable_flags as the parameter generated by test_cumprod once
    # this issue is marked as completed https://github.com/pytorch/pytorch/issues/75733
    if backend_fw == "torch":
        assume(not test_flags.as_variable[0])
    np_frontend_helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        x=x[0],
        axis=axis,
        dtype=dtype,
    )


# nancumprod
@handle_frontend_test(
    fn_tree="numpy.nancumprod",
    dtype_and_x_axis_dtype=_get_castable_dtypes_values(allow_nan=True),
)
def test_numpy_nancumprod(
    dtype_and_x_axis_dtype,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
):
    input_dtypes, x, axis, dtype = dtype_and_x_axis_dtype
    if backend_fw == "torch":
        assume(not test_flags.as_variable[0])
    np_frontend_helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        x=x[0],
        axis=axis,
        dtype=dtype,
    )


# nancumsum
@handle_frontend_test(
    fn_tree="numpy.nancumsum",
    dtype_and_x_axis_dtype=_get_castable_dtypes_values(allow_nan=True),
)
def test_numpy_nancumsum(
    dtype_and_x_axis_dtype,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
):
    input_dtypes, x, axis, dtype = dtype_and_x_axis_dtype
    if backend_fw == "torch":
        assume(not test_flags.as_variable[0])
    np_frontend_helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        x=x[0],
        axis=axis,
        dtype=dtype,
    )


# nanprod
@handle_frontend_test(
    fn_tree="numpy.nanprod",
    dtype_and_x_dtype=_get_castable_dtypes_values(allow_nan=True, use_where=True),
    keepdims=st.booleans(),
    initial=st.one_of(st.floats(min_value=-100, max_value=100)),
)
def test_numpy_nanprod(
    dtype_and_x_dtype,
    initial,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
    keepdims,
):
    input_dtypes, x, axis, dtype, where = dtype_and_x_dtype
    if backend_fw == "torch":
        assume(not test_flags.as_variable[0])
    where, input_dtypes, test_flags = np_frontend_helpers.handle_where_and_array_bools(
        where=where,
        input_dtype=input_dtypes,
        test_flags=test_flags,
    )
    np_frontend_helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        a=x[0],
        axis=axis,
        dtype=dtype,
        initial=initial,
        where=where,
        keepdims=keepdims,
    )


# nansum
@handle_frontend_test(
    fn_tree="numpy.nansum",
    dtype_and_x_dtype=_get_castable_dtypes_values(allow_nan=True, use_where=True),
    keepdims=st.booleans(),
    initial=st.one_of(st.floats(min_value=-100, max_value=100)),
)
def test_numpy_nansum(
    dtype_and_x_dtype,
    initial,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
    keepdims,
):
    input_dtypes, x, axis, dtype, where = dtype_and_x_dtype
    if backend_fw == "torch":
        assume(not test_flags.as_variable[0])
    where, input_dtypes, test_flags = np_frontend_helpers.handle_where_and_array_bools(
        where=where,
        input_dtype=input_dtypes,
        test_flags=test_flags,
    )
    np_frontend_helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        a=x[0],
        axis=axis,
        dtype=dtype,
        initial=initial,
        where=where,
        keepdims=keepdims,
    )


# diff
@handle_frontend_test(
    fn_tree="numpy.diff",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        min_num_dims=1,
        valid_axis=True,
        force_int_axis=True,
    ),
)
def test_numpy_diff(
    dtype_x_axis,
    frontend,
    test_flags,
    fn_tree,
    backend_fw,
    on_device,
):
    input_dtype, x, axis = dtype_x_axis
    np_frontend_helpers.test_frontend_function(
        input_dtypes=input_dtype,
        frontend=frontend,
        test_flags=test_flags,
        backend_to_test=backend_fw,
        fn_tree=fn_tree,
        on_device=on_device,
        x=x[0],
        axis=axis,
    )


# ediff1d
@handle_frontend_test(
    fn_tree="numpy.ediff1d",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"), min_num_dims=1, max_num_dims=1
    ),
    to_end=st.one_of(
        st.integers(-1, 10), st.lists(st.integers(-1, 10), min_size=1, max_size=10)
    ),
    to_begin=st.one_of(
        st.integers(-1, 10), st.lists(st.integers(-1, 10), min_size=1, max_size=10)
    ),
)
def test_numpy_ediff1d(
    *,
    dtype_and_x,
    on_device,
    fn_tree,
    frontend,
    test_flags,
    backend_fw,
    to_end,
    to_begin,
):
    input_dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        backend_to_test=backend_fw,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        test_flags=test_flags,
        ary=x[0],
        to_end=to_end,
        to_begin=to_begin,
    )


# trapz
@st.composite
def _either_x_dx(draw):
    rand = (draw(st.integers(min_value=0, max_value=1)),)
    if rand == 0:
        either_x_dx = draw(
            helpers.dtype_and_values(
                avaliable_dtypes=st.shared(
                    helpers.get_dtypes("float"), key="trapz_dtype"
                ),
                min_value=-100,
                max_value=100,
                min_num_dims=1,
                max_num_dims=3,
                min_dim_size=1,
                max_dim_size=3,
            )
        )
        return rand, either_x_dx
    else:
        either_x_dx = draw(
            st.floats(min_value=-10, max_value=10),
        )
        return rand, either_x_dx


@handle_frontend_test(
    fn_tree="numpy.trapz",
    dtype_values_axis=helpers.dtype_values_axis(
        available_dtypes=st.shared(helpers.get_dtypes("float"), key="trapz_dtype"),
        min_value=-100,
        max_value=100,
        min_num_dims=1,
        max_num_dims=3,
        min_dim_size=1,
        max_dim_size=3,
        allow_neg_axes=True,
        valid_axis=True,
        force_int_axis=True,
    ),
    rand_either=_either_x_dx(),
)
def test_numpy_trapz(
    dtype_values_axis,
    rand_either,
    fn_tree,
    frontend,
    test_flags,
    on_device,
    backend_fw,
):
    input_dtype, y, axis = dtype_values_axis
    rand, either_x_dx = rand_either
    if rand == 0:
        dtype_x, x = either_x_dx
        x = np.asarray(x, dtype=dtype_x)
        dx = None
    else:
        x = None
        dx = either_x_dx
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        backend_to_test=backend_fw,
        frontend=frontend,
        fn_tree=fn_tree,
        test_flags=test_flags,
        on_device=on_device,
        y=np.asarray(y[0], dtype=input_dtype[0]),
        x=x,
        dx=dx,
        axis=axis,
    )
