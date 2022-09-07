# global
import numpy as np
from hypothesis import given, strategies as st
import sys

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.tensorflow as ivy_tf
import ivy.functional.backends.numpy as ivy_np
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


@st.composite
def _get_dtype_and_matrix(draw):
    arbitrary_dims = draw(helpers.get_shape(max_dim_size=5))
    random_size = draw(st.integers(min_value=1, max_value=4))
    shape = (*arbitrary_dims, random_size, random_size)
    return draw(
        helpers.dtype_and_values(
            available_dtypes=ivy_tf.valid_float_dtypes,
            shape=shape,
            min_value=-10,
            max_value=10,
        )
    )


@given(
    dtype_and_input=_get_dtype_and_matrix(),
    as_variable=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.det"
    ),
    native_array=st.booleans(),
)
def test_tensorflow_det(
    dtype_and_input, as_variable, num_positional_args, native_array, fw
):
    input_dtype, x = dtype_and_input
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_tree="linalg.det",
        input=np.asarray(x, dtype=input_dtype),
    )


@given(
    dtype_and_input=_get_dtype_and_matrix(),
    as_variable=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.eigvalsh"
    ),
    native_array=st.booleans(),
)
def test_tensorflow_eigvalsh(
    dtype_and_input, as_variable, num_positional_args, native_array, fw
):
    input_dtype, x = dtype_and_input
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_tree="linalg.eigvalsh",
        input=np.asarray(x, dtype=input_dtype),
    )


@given(
    dtype_x=helpers.dtype_and_values(
        available_dtypes=ivy_np.valid_float_dtypes[1:],
        min_num_dims=2,
        min_value=-1e05,
        max_value=1e05,
    ),
    as_variables=st.booleans(),
    native_array=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.matrix_rank"
    ),
    tolr=st.floats(allow_nan=False, allow_infinity=False) | st.just(None),
    data=st.data(),
)
def test_matrix_rank(
    *, data, dtype_x, as_variables, num_positional_args, native_array, tolr, fw
):
    input_dtype, x = dtype_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variables,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_tree="linalg.matrix_rank",
        atol=1.0,
        a=np.asarray(x, dtype=input_dtype),
        tol=tolr,
    )


@st.composite
def _solve_get_dtype_and_data(draw):
    batch = draw(st.integers(min_value=1, max_value=5))
    random_size = draw(st.integers(min_value=2, max_value=4))
    # shape = (batch, random_size, random_size)

    input_dtype = draw(
        st.shared(st.sampled_from(ivy_tf.valid_float_dtypes), key="shared_dtype")
    )
    shape = (random_size, random_size)
    tmp = []
    for i in range(batch):
        tmp.append(
            draw(
                helpers.array_values(
                    dtype=input_dtype,
                    shape=shape,
                    min_value=-10,
                    max_value=10,
                ).filter(lambda x: np.linalg.cond(x) < 1 / sys.float_info.epsilon)
            )
        )

    data1 = (input_dtype, tmp)

    shape = (batch, random_size, draw(st.integers(min_value=2, max_value=4)))
    data2 = draw(
        helpers.dtype_and_values(
            available_dtypes=ivy_tf.valid_float_dtypes,
            shape=shape,
            min_value=-10,
            max_value=10,
        )
    )

    return data1, data2


# solve
@handle_cmd_line_args
@given(
    dtype_and_x=_solve_get_dtype_and_data(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.solve"
    ),
)
def test_tensorflow_solve(
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    data1, data2 = dtype_and_x
    input_dtype1, x = data1
    input_dtype2, y = data2

    helpers.test_frontend_function(
        input_dtypes=[input_dtype1, input_dtype2],
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_tree="linalg.solve",
        x=np.asarray(x, dtype=input_dtype1),
        y=np.asarray(y, dtype=input_dtype2),
    )


# slogdet
@given(
    dtype_and_x=_get_dtype_and_matrix(),
    as_variable=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.slogdet"
    ),
    native_array=st.booleans(),
)
def test_tensorflow_slogdet(
    *,
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_tree="linalg.slogdet",
        x=np.asarray(x, dtype=input_dtype),
    )


# cholesky_solve


@st.composite
def _get_cholesky_matrix(draw):
    # batch_shape, random_size, shared
    input_dtype = draw(
        st.shared(st.sampled_from(ivy_np.valid_float_dtypes), key="shared_dtype")
    )
    shared_size = draw(
        st.shared(helpers.ints(min_value=2, max_value=4), key="shared_size")
    )
    gen = draw(
        helpers.array_values(
            dtype=input_dtype,
            shape=tuple([shared_size, shared_size]),
            min_value=2,
            max_value=5,
        ).filter(lambda x: np.linalg.cond(x) < 1 / sys.float_info.epsilon)
    )

    spd = [np.matmul(np.array(elem), np.transpose(np.array(elem))) for elem in gen]
    spd_chol = [np.linalg.cholesky(np.array(elem)) for elem in spd]
    return input_dtype, spd_chol


@st.composite
def _get_second_matrix(draw):
    # batch_shape, shared, random_size
    input_dtype = draw(
        st.shared(st.sampled_from(ivy_np.valid_float_dtypes), key="shared_dtype")
    )
    shared_size = draw(
        st.shared(helpers.ints(min_value=2, max_value=4), key="shared_size")
    )
    return input_dtype, draw(
        helpers.array_values(
            dtype=input_dtype, shape=tuple([shared_size, 1]), min_value=2, max_value=5
        )
    )


@handle_cmd_line_args
@given(
    x=_get_cholesky_matrix(),
    y=_get_second_matrix(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.cholesky_solve"
    ),
)
def test_tensorflow_cholesky_solve(
    *,
    x,
    y,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype1, x1 = x
    input_dtype2, x2 = y

    helpers.test_frontend_function(
        input_dtypes=[input_dtype1, input_dtype2],
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_tree="linalg.cholesky_solve",
        rtol=1e-2,
        atol=1e-2,
        chol=np.asarray(x1, dtype=input_dtype1),
        rhs=np.asarray(x2, dtype=input_dtype2),
    )


# pinv
@given(
    dtype_and_input=_get_dtype_and_matrix(),
    as_variable=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.pinv"
    ),
    native_array=st.booleans(),
)
def test_tensorflow_pinv(
    dtype_and_input, as_variable, num_positional_args, native_array, fw
):
    input_dtype, x = dtype_and_input

    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_tree="linalg.pinv",
        a=np.asarray(x, dtype=input_dtype),
        rcond=1e-15,
        validate_args=False,
        name=None,
    )
