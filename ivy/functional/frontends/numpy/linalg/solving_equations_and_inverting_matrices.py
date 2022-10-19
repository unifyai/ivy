# local
import ivy
from ivy.functional.frontends.numpy.func_wrapper import to_ivy_arrays_and_back
from ... import versions
from ivy.func_wrapper import with_unsupported_dtypes
from ivy.functional.frontends.numpy import promote_types_of_numpy_inputs

version = versions["numpy"]


# solve
@with_unsupported_dtypes({"1.23.0 and below": ("float16",)}, version)
@to_ivy_arrays_and_back
def solve(a, b):
    a, b = promote_types_of_numpy_inputs(a, b)
    return ivy.solve(a, b)


# inv
@to_ivy_arrays_and_back
def inv(a):
    return ivy.inv(a)


# pinv
@to_ivy_arrays_and_back
def pinv(a, rtol=1e-15, hermitian=False):
    return ivy.pinv(a, rtol=rtol)


# tensorinv
@to_ivy_arrays_and_back
def tensorinv(a, ind=2):
    return ivy.tensorinv(a, ind=ind)
