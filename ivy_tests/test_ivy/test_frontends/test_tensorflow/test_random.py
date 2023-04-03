from hypothesis import strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test
import ivy

# random_sample
@handle_frontend_test(
    fn_tree="tensorflow.random.uniform",
    shape=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("integer"),
        min_value=1,
        max_value=5,
        min_num_dims=1,
        max_num_dims=1,
    ),
    minval=helpers.ints(min_value=0, max_value=3),
    maxval=helpers.ints(min_value=4, max_value=10),
    dtype=helpers.get_dtypes("float", full=False),
    seed=helpers.ints(min_value=0, max_value=10),
    test_with_out=st.just(False),
)
def test_tensorflow_uniform(
    shape,
    minval,
    maxval,
    dtype,
    seed,
    frontend,
    test_flags,
    fn_tree,
    on_device,
):

    input_dtypes, shape = shape
    helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=False,
        shape=shape[0],
        minval=minval,
        maxval=maxval,
        dtype=dtype[0],
        seed=seed,
    )


# random_normal
@handle_frontend_test(
    fn_tree="tensorflow.random.normal",
    shape=helpers.get_shape(
        allow_none=False,
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=10,
    ),
    mean=st.floats(allow_nan=False, allow_infinity=False, width=32),
    stddev=st.floats(allow_nan=False, allow_infinity=False, width=32, min_value=0),
    dtype=helpers.get_dtypes("float", full=False),
    seed=helpers.ints(min_value=0, max_value=10),
    test_with_out=st.just(False),
)
def test_tensorflow_normal(
    frontend,
    fn_tree,
    on_device,
    shape,
    mean,
    stddev,
    dtype,
    seed,
    test_flags,
):

    helpers.test_frontend_function(
        input_dtypes=dtype,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=False,
        shape=shape,
        mean=mean,
        stddev=stddev,
        dtype=dtype[0],
        seed=seed,
    )


# random_shuffle
@handle_frontend_test(
    fn_tree="tensorflow.random.shuffle",
    dtype_value=helpers.dtype_and_values(available_dtypes=helpers.get_dtypes("valid")),
    seed=helpers.ints(min_value=0, max_value=10),
    test_with_out=st.just(False),
)
def test_tensorflow_shuffle(
    frontend,
    fn_tree,
    on_device,
    dtype_value,
    seed,
    test_flags,
):
    input_dtypes, values = dtype_value
    helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=False,
        value=values[0],
        seed=seed,
    )


#random_stateless_uniform
@handle_frontend_test(
    fn_tree="tensorflow.random.stateless_uniform",
    shape=helpers.dtype_and_values(
        available_dtypes=tuple([ivy.int64, ivy.int32]),
        min_value=1,
        max_value=5,
        min_num_dims=1,
        max_num_dims=1,
    ),
    seed=helpers.dtype_and_values(
        available_dtypes=tuple([ivy.int64, ivy.int32]),
        min_value=0,
        max_value=10,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
        max_dim_size=2
    ),
    minval=helpers.ints(min_value=0, max_value=3),
    maxval=helpers.ints(min_value=4, max_value=10),
    dtype=helpers.get_dtypes("numeric", full=False),
    test_with_out=st.just(False),
)
def test_tensorflow_stateless_uniform(
    shape,
    seed,
    minval,
    maxval,
    dtype,
    frontend,
    test_flags,
    fn_tree,
    on_device,
):
    if('complex' in dtype[0] or 'int8' in dtype[0] or 'int16' in dtype[0] or 'uint' in dtype[0]):
        return

    shape_input_dtypes, shape = shape
    seed_input_dtypes, seed = seed

    if(len(seed[0]) < 2):
        return

    print(seed[0])
    print(dtype[0])

    helpers.test_frontend_function(
        input_dtypes=shape_input_dtypes,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=False,
        shape=shape[0],
        seed=(seed[0][0], seed[0][1]),
        minval=minval,
        maxval=maxval,
        dtype=dtype[0]
    )

