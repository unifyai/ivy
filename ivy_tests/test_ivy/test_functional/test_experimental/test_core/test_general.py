# global
from hypothesis import strategies as st

# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_test


# --- Helpers --- #
# --------------- #


@st.composite
def _reduce_helper(draw):
    # ToDo: remove the filtering when supported dtypes are fixed for mixed functions
    dtype = draw(
        helpers.get_dtypes("valid", full=False).filter(lambda x: "complex" not in x[0])
    )
    if dtype[0] == "bool":
        func = draw(st.sampled_from([ivy.logical_and, ivy.logical_or]))
    else:
        func = draw(st.sampled_from([ivy.add, ivy.maximum, ivy.minimum, ivy.multiply]))
    init_value = draw(
        helpers.dtype_and_values(
            dtype=dtype,
            shape=(),
            allow_inf=True,
        )
    )[1]
    dtype, operand, shape = draw(
        helpers.dtype_and_values(
            min_num_dims=1,
            dtype=dtype,
            ret_shape=True,
        )
    )
    axes = draw(helpers.get_axis(shape=shape))
    return dtype, operand[0], init_value[0], func, axes


# --- Main --- #
# ------------ #


# reduce
@handle_test(
    fn_tree="functional.ivy.experimental.reduce",
    args=_reduce_helper(),
    keepdims=st.booleans(),
    test_with_out=st.just(False),
    test_gradients=st.just(False),
)
def test_reduce(*, args, keepdims, test_flags, backend_fw, fn_name, on_device):
    dtype, operand, init_value, func, axes = args
    helpers.test_function(
        input_dtypes=dtype,
        test_flags=test_flags,
        backend_to_test=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        operand=operand,
        init_value=init_value,
        computation=func,
        axes=axes,
        keepdims=keepdims,
    )


@handle_test(
    fn_tree="functional.ivy.experimental.sequence_length",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=["float64", "int8", "bool", "complex64", "int32"],
        min_value=-10,
        max_value=10,
        num_arrays=3,
        shared_dtype=True,
    ),
    test_with_out=st.just(False),
)
def test_sequence_length(dtype_and_x, test_flags, backend_fw, fn_name, on_device):
    dtype, x = dtype_and_x
    helpers.test_function(
        input_dtypes=dtype,
        test_flags=test_flags,
        on_device=on_device,
        num_positional_args=2,
        backend_to_test=backend_fw,
        fn_name=fn_name,
        test_values=True,
        x=x,
    )
