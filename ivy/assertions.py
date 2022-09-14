import ivy
import builtins


# General #
# ------- #


def check_elem_in_list(elem, list):
    if elem not in list:
        raise ivy.exceptions.IvyException("{} must be one of {}".format(elem, list))


def check_less(x1, x2, allow_equal=False):
    if allow_equal and ivy.any(x1 > x2):
        raise ivy.exceptions.IvyException(
            "{} must be lesser than or equal to {}".format(x1, x2)
        )
    elif not allow_equal and ivy.any(x1 >= x2):
        raise ivy.exceptions.IvyException("{} must be lesser than {}".format(x1, x2))


def check_greater(x1, x2, allow_equal=False):
    if allow_equal and ivy.any(x1 < x2):
        raise ivy.exceptions.IvyException(
            "{} must be greater than or equal to {}".format(x1, x2)
        )
    elif not allow_equal and ivy.any(x1 <= x2):
        raise ivy.exceptions.IvyException("{} must be greater than {}".format(x1, x2))


def check_equal(x1, x2, inverse=False):
    if inverse and ivy.any(x1 == x2):
        raise ivy.exceptions.IvyException("{} must not be equal to {}".format(x1, x2))
    elif not inverse and ivy.any(x1 != x2):
        raise ivy.exceptions.IvyException("{} must be equal to {}".format(x1, x2))


def check_isinstance(x, allowed_types):
    if not isinstance(x, allowed_types):
        raise ivy.exceptions.IvyException(
            "type of x: {} must be one of the allowed types: {}".format(
                type(x), allowed_types
            )
        )


# General with Custom Message #
# --------------------------- #


def check_true(expression, message="expression must be True"):
    if not expression:
        raise ivy.exceptions.IvyException(message)


def check_false(expression, message="expression must be False"):
    if expression:
        raise ivy.exceptions.IvyException(message)


def check_all(results, message="one of the args is False"):
    if not builtins.all(results):
        raise ivy.exceptions.IvyException(message)


def check_any(results, message="all of the args are False"):
    if not builtins.any(results):
        raise ivy.exceptions.IvyException(message)


def check_all_or_any_fn(
    *args,
    fn,
    type="all",
    limit=[0],
    message="args must exist according to type and limit given"
):
    if type == "all":
        check_all([fn(arg) for arg in args], message)
    elif type == "any":
        count = 0
        for arg in args:
            count = count + 1 if fn(arg) else count
        if count not in limit:
            raise ivy.exceptions.IvyException(message)
    else:
        raise ivy.exceptions.IvyException("type must be all or any")


# Creation #
# -------- #


def check_fill_value_and_dtype_are_compatible(fill_value, dtype):
    if not (
        (ivy.is_int_dtype(dtype) or ivy.is_uint_dtype(dtype))
        and isinstance(fill_value, int)
    ) and not (
        ivy.is_float_dtype(dtype)
        and isinstance(fill_value, float)
        or isinstance(fill_value, bool)
    ):
        raise ivy.exceptions.IvyException(
            "the fill_value: {} and data type: {} are not compatible".format(
                fill_value, dtype
            )
        )
