# global
import ivy


def add(x, y, name=None):
    return ivy.add(x, y)


add.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def tan(x, name=None):
    return ivy.tan(x)


tan.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def concat(values, axis, name="concat"):
    return ivy.concat(values, axis)


def linear(x):
    return ivy.linear(x)

def Exponential(x):
    return ivy.exponential(x)

def hard_sigmoid(x):
    return ivy.array.hard_sigmoid(x)