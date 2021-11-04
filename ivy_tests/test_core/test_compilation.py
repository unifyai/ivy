"""
Collection of tests for templated general functions
"""

# global
import time
import pytest
import numpy as np
from numbers import Number

# local
import ivy
import ivy.numpy
import ivy_tests.helpers as helpers


# Tests #
# ------#

# in-place

# functions to compile
def _fn_1(x, with_non_compiled: bool = False):
    for _ in range(100000):
        pass
    if with_non_compiled:
        (x + 3) * 4  # ops not to be compiled into the graph
    return x**2


def _fn_2(x, with_non_compiled: bool = False):
    for _ in range(100000):
        pass
    if with_non_compiled:
        (x + 3) * 4  # ops not to be compiled into the graph
    return (x + 10)**0.5 - 5


@pytest.mark.parametrize(
    "x", [[1], [[0.0, 1.0], [2.0, 3.0]]])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
@pytest.mark.parametrize(
    "tensor_fn", [ivy.array, helpers.var_fn])
def test_compile(x, dtype_str, tensor_fn, dev_str, call):
    if ivy.wrapped_mode():
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    # smoke test
    if (isinstance(x, Number) or len(x) == 0) and tensor_fn == helpers.var_fn and call is helpers.mx_call:
        # mxnet does not support 0-dimensional variables
        pytest.skip()

    # function 1
    comp_fn = ivy.compile(_fn_1)
    # type test
    assert callable(comp_fn)
    # value test
    x = tensor_fn(x, dtype_str, dev_str)
    non_compiled_return = _fn_1(x)
    x = tensor_fn(x, dtype_str, dev_str)
    compiled_return = comp_fn(x)
    assert np.allclose(ivy.to_numpy(non_compiled_return), ivy.to_numpy(compiled_return))

    # function 2
    comp_fn = ivy.compile(_fn_2)
    # type test
    assert callable(comp_fn)
    # value test
    x = tensor_fn(x, dtype_str, dev_str)
    non_compiled_return = _fn_2(x)
    x = tensor_fn(x, dtype_str, dev_str)
    compiled_return = comp_fn(x)
    assert np.allclose(ivy.to_numpy(non_compiled_return), ivy.to_numpy(compiled_return))


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "x_raw", [[1]])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
@pytest.mark.parametrize(
    "tensor_fn", [ivy.array])
@pytest.mark.parametrize(
    "with_non_compiled", [True, False])
def test_compile_graph_inplace(x_raw, dtype_str, tensor_fn, with_non_compiled, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # smoke test
    if (isinstance(x_raw, Number) or len(x_raw) == 0) and tensor_fn == helpers.var_fn and call is helpers.mx_call:
        # mxnet does not support 0-dimensional variables
        pytest.skip()

    # function 1
    x = tensor_fn(x_raw, dtype_str, dev_str)
    ivy.show_graph(_fn_1, x, with_non_compiled, output_connected_only=False,
                   fname='fn1_inplace_{}.png'.format(with_non_compiled))
    comp_fn = ivy.compile_graph(_fn_1, x, with_non_compiled)
    # type test
    assert callable(comp_fn)
    # value test
    start_time = time.perf_counter()
    x = tensor_fn(x_raw, dtype_str, dev_str)
    non_compiled_return = _fn_1(x, with_non_compiled)
    non_comp_time_taken = time.perf_counter() - start_time
    assert len(comp_fn.__self__._all_param_dict) == 2
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 1
    start_time = time.perf_counter()
    x = tensor_fn(x_raw, dtype_str, dev_str)
    compiled_return = comp_fn(x, with_non_compiled)
    comp_time_taken = time.perf_counter() - start_time
    assert len(comp_fn.__self__._all_param_dict) == 2
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 1
    assert np.allclose(ivy.to_numpy(non_compiled_return), ivy.to_numpy(compiled_return))
    assert comp_time_taken < non_comp_time_taken

    # function 2
    x = tensor_fn(x_raw, dtype_str, dev_str)
    ivy.show_graph(_fn_2, x, with_non_compiled, output_connected_only=False,
                   fname='fn2_inplace_{}.png'.format(with_non_compiled))
    comp_fn = ivy.compile_graph(_fn_2, x, with_non_compiled)
    # type test
    assert callable(comp_fn)
    # value test
    start_time = time.perf_counter()
    x = tensor_fn(x_raw, dtype_str, dev_str)
    non_compiled_return = _fn_2(x, with_non_compiled)
    non_comp_time_taken = time.perf_counter() - start_time
    assert len(comp_fn.__self__._all_param_dict) == 4
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 3
    start_time = time.perf_counter()
    x = tensor_fn(x_raw, dtype_str, dev_str)
    compiled_return = comp_fn(x, with_non_compiled)
    comp_time_taken = time.perf_counter() - start_time
    assert len(comp_fn.__self__._all_param_dict) == 4
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 3
    assert np.allclose(ivy.to_numpy(non_compiled_return), ivy.to_numpy(compiled_return))
    assert comp_time_taken < non_comp_time_taken


# functional

def _fn_3(x, with_non_compiled: bool = False, with_internal_gen: bool = False):
    if with_internal_gen:
        x += ivy.array([1.])
    time.sleep(0.05)
    if with_non_compiled:
        (x + 3) * 4  # ops not to be compiled into the graph
    return ivy.reduce_mean(ivy.reduce_sum(x, keepdims=True), keepdims=True)


def _fn_4(x, with_non_compiled: bool = False, with_internal_gen: bool = False):
    if with_internal_gen:
        x += ivy.array([1.])
    y = ivy.reduce_mean(x)
    z = ivy.reduce_sum(x)
    f = ivy.reduce_var(y)
    time.sleep(0.05)
    k = ivy.cos(z)
    m = ivy.sin(f)
    o = ivy.tan(y)
    if with_non_compiled:
        (x + 3) * 4  # ops not to be compiled into the graph
    return ivy.concatenate([k, m, o], -1)


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "x_raw", [[1]])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
@pytest.mark.parametrize(
    "tensor_fn", [ivy.array])
@pytest.mark.parametrize(
    "with_non_compiled", [True, False])
@pytest.mark.parametrize(
    "with_internal_gen", [True, False])
def test_compile_graph(x_raw, dtype_str, tensor_fn, with_non_compiled, with_internal_gen, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # smoke test
    if (isinstance(x_raw, Number) or len(x_raw) == 0) and tensor_fn == helpers.var_fn and call is helpers.mx_call:
        # mxnet does not support 0-dimensional variables
        pytest.skip()

    # function 3
    x = tensor_fn(x_raw, dtype_str, dev_str)
    ivy.show_graph(_fn_3, x, with_non_compiled, with_internal_gen, output_connected_only=False,
                   fname='fn3_{}_{}.png'.format(with_non_compiled, with_internal_gen))
    comp_fn = ivy.compile_graph(_fn_3, x, with_non_compiled, with_internal_gen)
    # type test
    assert callable(comp_fn)
    # value test
    start_time = time.perf_counter()
    x = tensor_fn(x_raw, dtype_str, dev_str)
    non_compiled_return = _fn_3(x, with_non_compiled, with_internal_gen)
    non_comp_time_taken = time.perf_counter() - start_time
    assert len(comp_fn.__self__._all_param_dict) == 3 + (1 if with_internal_gen else 0)
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 2 + (1 if with_internal_gen else 0)
    start_time = time.perf_counter()
    x = tensor_fn(x_raw, dtype_str, dev_str)
    compiled_return = comp_fn(x, with_non_compiled, with_internal_gen)
    comp_time_taken = time.perf_counter() - start_time
    assert len(comp_fn.__self__._all_param_dict) == 3 + (1 if with_internal_gen else 0)
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 2 + (1 if with_internal_gen else 0)
    assert np.allclose(ivy.to_numpy(non_compiled_return), ivy.to_numpy(compiled_return))
    assert comp_time_taken < non_comp_time_taken

    # function 4
    x = tensor_fn(x_raw, dtype_str, dev_str)
    ivy.show_graph(_fn_4, x, with_non_compiled, with_internal_gen, output_connected_only=False,
                   fname='fn4_{}_{}.png'.format(with_non_compiled, with_internal_gen))
    comp_fn = ivy.compile_graph(_fn_4, x, with_non_compiled, with_internal_gen)
    # type test
    assert callable(comp_fn)
    # value test
    start_time = time.perf_counter()
    x = tensor_fn(x_raw, dtype_str, dev_str)
    non_compiled_return = _fn_4(x, with_non_compiled, with_internal_gen)
    non_comp_time_taken = time.perf_counter() - start_time
    assert len(comp_fn.__self__._all_param_dict) == 11 + (1 if with_internal_gen else 0)
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 10 + (1 if with_internal_gen else 0)
    start_time = time.perf_counter()
    x = tensor_fn(x_raw, dtype_str, dev_str)
    compiled_return = comp_fn(x, with_non_compiled, with_internal_gen)
    comp_time_taken = time.perf_counter() - start_time
    assert len(comp_fn.__self__._all_param_dict) == 11 + (1 if with_internal_gen else 0)
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 10 + (1 if with_internal_gen else 0)
    assert np.allclose(ivy.to_numpy(non_compiled_return), ivy.to_numpy(compiled_return))
    assert comp_time_taken < non_comp_time_taken


# random

def _rand_fn(x, with_non_compiled: bool = False):
    if with_non_compiled:
        (x + 3) * 4  # ops not to be compiled into the graph
    return x + ivy.random_uniform(0., 1., x.shape)


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "x_raw", [[1]])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
@pytest.mark.parametrize(
    "tensor_fn", [ivy.array])
@pytest.mark.parametrize(
    "with_non_compiled", [True, False])
def test_compile_graph_w_random(x_raw, dtype_str, tensor_fn, with_non_compiled, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # smoke test
    if (isinstance(x_raw, Number) or len(x_raw) == 0) and tensor_fn == helpers.var_fn and call is helpers.mx_call:
        # mxnet does not support 0-dimensional variables
        pytest.skip()

    # random function
    x = tensor_fn(x_raw, dtype_str, dev_str)
    ivy.show_graph(_rand_fn, x, with_non_compiled, output_connected_only=False,
                   fname='w_random_{}.png'.format(with_non_compiled))
    comp_fn = ivy.compile_graph(_rand_fn, x, with_non_compiled)
    # type test
    assert callable(comp_fn)
    # value test
    x = tensor_fn(x_raw, dtype_str, dev_str)
    nc_return0 = _rand_fn(x, with_non_compiled)
    nc_return1 = _rand_fn(x, with_non_compiled)
    assert nc_return0 != nc_return1
    assert len(comp_fn.__self__._all_param_dict) == 5
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 4
    x = tensor_fn(x_raw, dtype_str, dev_str)
    c_return0 = comp_fn(x, with_non_compiled)
    c_return1 = comp_fn(x, with_non_compiled)
    assert c_return0 != c_return1
    assert len(comp_fn.__self__._all_param_dict) == 5
    assert comp_fn.__self__.params_all_empty()
    assert len(list(comp_fn.__self__._all_functions)) == 4


# detached divide

def _detach_div_fn(x):
    return x + (ivy.array([1.]) / ivy.array([2.]))


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "x_raw", [[1]])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
@pytest.mark.parametrize(
    "tensor_fn", [ivy.array])
def test_compile_graph_w_detached_divide(x_raw, dtype_str, tensor_fn, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # smoke test
    if (isinstance(x_raw, Number) or len(x_raw) == 0) and tensor_fn == helpers.var_fn and call is helpers.mx_call:
        # mxnet does not support 0-dimensional variables
        pytest.skip()

    # detached divide function
    x = tensor_fn(x_raw, dtype_str, dev_str)
    ivy.show_graph(_detach_div_fn, x, output_connected_only=False,
                   fname='w_detached_divide.png')
    comp_fn = ivy.compile_graph(_detach_div_fn, x)
    # type test
    assert callable(comp_fn)
    # value test
    x = tensor_fn(x_raw, dtype_str, dev_str)
    nc_return = _detach_div_fn(x)
    x = tensor_fn(x_raw, dtype_str, dev_str)
    c_return = comp_fn(x)
    assert np.allclose(ivy.to_numpy(nc_return), ivy.to_numpy(c_return))


# input in output

def _input_in_output(x, y):
    return x + 2, y


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "x_raw", [[1]])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
@pytest.mark.parametrize(
    "tensor_fn", [ivy.array])
def test_compile_graph_input_in_output(x_raw, dtype_str, tensor_fn, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # smoke test
    if (isinstance(x_raw, Number) or len(x_raw) == 0) and tensor_fn == helpers.var_fn and call is helpers.mx_call:
        # mxnet does not support 0-dimensional variables
        pytest.skip()

    # detached divide function
    x = tensor_fn(x_raw, dtype_str, dev_str)
    y = tensor_fn(x_raw, dtype_str, dev_str)
    ivy.show_graph(_input_in_output, x, y, output_connected_only=False,
                   fname='input_in_output.png')
    comp_fn = ivy.compile_graph(_input_in_output, x, y)
    # type test
    assert callable(comp_fn)
    # value test
    x = tensor_fn(x_raw, dtype_str, dev_str)
    nc_ret_a, nc_ret_b = _input_in_output(x, y)
    x = tensor_fn(x_raw, dtype_str, dev_str)
    c_ret_a, c_ret_b = comp_fn(x, y)
    assert np.allclose(ivy.to_numpy(nc_ret_a), ivy.to_numpy(c_ret_a))
    assert np.allclose(ivy.to_numpy(nc_ret_b), ivy.to_numpy(c_ret_b))


# inplace variable update

def _inplace_var_update(weight, grad):
    weight.data -= grad
    return weight


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "weight_n_grad", [([1], [2])])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
def test_compile_graph_inplace_var_update(weight_n_grad, dtype_str, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # raw values
    weight_raw, grad_raw = weight_n_grad
    # as tensors
    weight = ivy.variable(ivy.array(weight_raw, dtype_str, dev_str))
    # compile
    ivy.show_graph(_inplace_var_update, weight, ivy.copy_array(weight), output_connected_only=False,
                   fname='inplace_var_update.png')
    comp_fn = ivy.compile_graph(_inplace_var_update, weight, ivy.copy_array(weight))
    # type test
    assert callable(comp_fn)
    # value test
    nc_weight = ivy.variable(ivy.array(weight_raw, dtype_str, dev_str))
    grad = ivy.array(grad_raw, dtype_str, dev_str)
    nc_new_weight = _inplace_var_update(nc_weight, grad)
    c_weight = ivy.variable(ivy.array(weight_raw, dtype_str, dev_str))
    grad = ivy.array(grad_raw, dtype_str, dev_str)
    c_new_weight = comp_fn(c_weight, grad)
    assert not np.allclose(np.asarray(weight_raw), ivy.to_numpy(nc_new_weight))
    assert not np.allclose(np.asarray(weight_raw), ivy.to_numpy(c_new_weight))
    assert np.allclose(ivy.to_numpy(nc_new_weight), ivy.to_numpy(c_new_weight))


# with stateful


class Stateful:

    def __init__(self):
        self._state = ivy.array([0.])

    # noinspection PyAugmentAssignment
    def forward(self, _x):
        self._state = self._state + 1
        return _x + self._state

    def compile_graph(self, _x):
        ivy.show_graph(self.forward, _x, stateful=[self], output_connected_only=False,
                       fname='w_stateful.png')
        # noinspection PyAttributeOutsideInit
        self.forward = ivy.compile_graph(self.forward, _x, stateful=[self])

    def __setattr__(self, key, value):
        self.__dict__[key] = value


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "x_raw", [([0])])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
def test_compile_graph_w_stateful(x_raw, dtype_str, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # as tensors
    x = ivy.array(x_raw, dtype_str, dev_str)

    # non-compiled
    stateful = Stateful()
    nc_ret_0 = stateful.forward(x)
    assert nc_ret_0 == x + 1
    nc_ret_1 = stateful.forward(x)
    assert nc_ret_1 == x + 2
    nc_ret_2 = stateful.forward(x)
    assert nc_ret_2 == x + 3

    # compiled
    stateful = Stateful()
    stateful.compile_graph(x)
    c_ret_0 = stateful.forward(x)
    assert c_ret_0 == x + 1
    c_ret_1 = stateful.forward(x)
    assert c_ret_1 == x + 2
    c_ret_2 = stateful.forward(x)
    assert c_ret_2 == x + 3


'''
# with stateful container

def _update_container(cont, x):
    cont.new_attribute = 2
    return x + 1


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "x_raw", [([0])])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
def test_compile_graph_w_stateful_cont(x_raw, dtype_str, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # as tensors
    x = ivy.array(x_raw, dtype_str, dev_str)

    # non-compiled
    cont = ivy.Container(x=x)
    assert not hasattr(cont, 'new_attribute')
    nc_ret_0 = _update_container(cont, x)
    assert nc_ret_0 == x + 1
    assert hasattr(cont, 'new_attribute')
    assert cont.new_attribute == 2

    # compiled
    cont = ivy.Container(x=x)
    comp_fn = ivy.compile_graph(_update_container, cont.deep_copy(), x, arg_stateful_idxs=[[0]])
    assert not hasattr(cont, 'new_attribute')
    c_ret_0 = comp_fn(cont, x)
    assert c_ret_0 == x + 1
    assert hasattr(cont, 'new_attribute')
    assert cont.new_attribute == 2
'''


# with stateful in args

class StatefulInArg:

    def __init__(self):
        self._state = ivy.array([0.])

    def add_one(self):
        self._state += 1

    @property
    def state(self):
        return self._state

def _stateful_in_arg_method(x, sia):
    x = x + 1
    sia.add_one()
    return x


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "x_raw", [([0])])
@pytest.mark.parametrize(
    "dtype_str", ['float32'])
def test_compile_graph_w_stateful_in_args(x_raw, dtype_str, dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # as tensors
    x = ivy.array(x_raw, dtype_str, dev_str)
    sia = StatefulInArg()
    # compile
    ivy.show_graph(_stateful_in_arg_method, x, sia, arg_stateful_idxs=[[1]], output_connected_only=False,
                   fname='w_stateful_in_args.png')
    comp_fn = ivy.compile_graph(_stateful_in_arg_method, x, sia, arg_stateful_idxs=[[1]])
    # type test
    assert callable(comp_fn)
    # value test
    ret = comp_fn(x, sia)
    assert ret == 1
    assert sia.state == 1


# reverse built-in

def _rev_builtin(x):
    return 10. ** x


def test_compile_graph_reverse_builtin(dev_str, compile_graph, call):
    if ivy.wrapped_mode() or not compile_graph:
        # Wrapped mode does not yet support function compilation
        pytest.skip()
    if call is not helpers.torch_call:
        # currently only supported by PyTorch
        pytest.skip()
    # config
    x = ivy.array([0., 1., 2.])
    # compile
    ivy.show_graph(_rev_builtin, x, output_connected_only=False, fname='rev_builtin.png')
    comp_fn = ivy.compile_graph(_rev_builtin, x)
    # type test
    assert callable(comp_fn)
    # value test
    nc_ret = _rev_builtin(x)
    c_ret = comp_fn(x)
    assert np.allclose(ivy.to_numpy(nc_ret), ivy.to_numpy(c_ret))
