@@ -1,35 +1,35 @@
# global
from hypothesis import strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


# hann_window
@handle_frontend_test(
    fn_tree="torch.hann_window",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        max_num_dims=0,
        min_value=5,
        max_value=10,
    ),
    periodic=st.booleans(),
    test_with_out=st.just(False),
)
def test_torch_hann_window(
    *, dtype_and_x, test_flags, backend_fw, fn_tree, on_device, frontend, periodic
):      
    input_dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        backend_to_test=backend_fw,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        atol=1e-02,
        window_length=int(x[0]),
        periodic=periodic,
    )
