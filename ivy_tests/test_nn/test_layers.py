"""
Collection of tests for templated neural network layers
"""

# global
import pytest
import numpy as np

# local
import ivy
import ivy_tests.helpers as helpers
from ivy.core.container import Container


# Linear #
# -------#

# linear
@pytest.mark.parametrize(
    "bs_ic_oc_target", [
        ([1, 2], 4, 5, [[0.30230279, 0.65123089, 0.30132881, -0.90954636, 1.08810135]]),
    ])
@pytest.mark.parametrize(
    "with_v", [True, False])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
@pytest.mark.parametrize(
    "tensor_fn", [ivy.array, helpers.var_fn])
def test_linear_layer(bs_ic_oc_target, with_v, dtype_str, tensor_fn, dev_str, call):
    # smoke test
    batch_shape, input_channels, output_channels, target = bs_ic_oc_target
    x = ivy.cast(ivy.linspace(ivy.zeros(batch_shape), ivy.ones(batch_shape), input_channels), 'float32')
    if with_v:
        np.random.seed(0)
        wlim = (6 / (output_channels + input_channels)) ** 0.5
        w = ivy.variable(ivy.array(np.random.uniform(-wlim, wlim, (output_channels, input_channels)), 'float32'))
        b = ivy.variable(ivy.zeros([output_channels]))
        v = Container({'w': w, 'b': b})
    else:
        v = None
    linear_layer = ivy.Linear(input_channels, output_channels, v)
    ret = linear_layer(x)
    # type test
    assert isinstance(ret, ivy.Array)
    # cardinality test
    assert ret.shape == tuple(batch_shape + [output_channels])
    # value test
    if not with_v:
        return
    assert np.allclose(call(linear_layer, x), np.array(target))
    # compilation test
    if call is helpers.torch_call:
        # pytest scripting does not **kwargs
        return
    helpers.assert_compilable(linear_layer)


# LSTM #
# -----#

# lstm
@pytest.mark.parametrize(
    "b_t_ic_hc_otf_sctv", [
        (2, 3, 4, 5, [0.93137765, 0.9587628, 0.96644664, 0.93137765, 0.9587628, 0.96644664], 3.708991),
    ])
@pytest.mark.parametrize(
    "with_v", [True, False])
@pytest.mark.parametrize(
    "with_initial_state", [True, False])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
@pytest.mark.parametrize(
    "tensor_fn", [ivy.array, helpers.var_fn])
def test_lstm_layer(b_t_ic_hc_otf_sctv, with_v, with_initial_state, dtype_str, tensor_fn, dev_str, call):
    # smoke test
    b, t, input_channels, hidden_channels, output_true_flat, state_c_true_val = b_t_ic_hc_otf_sctv
    x = ivy.cast(ivy.linspace(ivy.zeros([b, t]), ivy.ones([b, t]), input_channels), 'float32')
    if with_initial_state:
        init_h = ivy.ones([b, hidden_channels])
        init_c = ivy.ones([b, hidden_channels])
        initial_state = ([init_h], [init_c])
    else:
        initial_state = None
    if with_v:
        kernel = ivy.variable(ivy.ones([input_channels, 4*hidden_channels]))*0.5
        recurrent_kernel = ivy.variable(ivy.ones([hidden_channels, 4*hidden_channels]))*0.5
        v = Container({'input': {'layer_0': {'w': kernel}},
                       'recurrent': {'layer_0': {'w': recurrent_kernel}}})
    else:
        v = None
    lstm_layer = ivy.LSTM(input_channels, hidden_channels, v=v)
    output, (state_h, state_c) = lstm_layer(x, initial_state=initial_state)
    # type test
    assert isinstance(output, ivy.Array)
    assert isinstance(state_h[0], ivy.Array)
    assert isinstance(state_c[0], ivy.Array)
    # cardinality test
    assert output.shape == (b, t, hidden_channels)
    assert state_h[0].shape == (b, hidden_channels)
    assert state_c[0].shape == (b, hidden_channels)
    # value test
    if not with_v or not with_initial_state:
        return
    output_true = np.tile(np.asarray(output_true_flat).reshape((b, t, 1)), (1, 1, hidden_channels))
    state_c_true = np.ones([b, hidden_channels]) * state_c_true_val
    output, (state_h, state_c) = call(lstm_layer, x, initial_state=initial_state)
    assert np.allclose(output, output_true, atol=1e-6)
    assert np.allclose(state_c, state_c_true, atol=1e-6)
    # compilation test
    if call in [helpers.torch_call]:
        # this is not a backend implemented function
        pytest.skip()
    helpers.assert_compilable(ivy.lstm_update)
