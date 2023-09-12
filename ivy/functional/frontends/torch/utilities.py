import ivy
from ivy.functional.frontends.torch.func_wrapper import to_ivy_arrays_and_back
from ivy.func_wrapper import with_supported_dtypes


# --- Helpers --- #
# --------------- #


@to_ivy_arrays_and_back
def _assert(condition, message):
    if not condition:
        raise Exception(message)
    else:
        return True


# --- Main --- #
# ------------ #


@with_supported_dtypes({"2.0.1": ("int64",)}, "torch")
@to_ivy_arrays_and_back
def bincount(x, weights=None, minlength=0):
    return ivy.bincount(x, weights=weights, minlength=minlength)


@to_ivy_arrays_and_back
def result_type(tensor, other):
    return ivy.result_type(tensor, other)
