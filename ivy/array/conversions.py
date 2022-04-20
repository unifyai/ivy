"""
Collection of Ivy functions for wrapping functions to accept and return ivy.Array instances.
"""

# global
from typing import Any, Union, Tuple, Dict, Iterable

# local
import ivy


# Helpers #
# --------#

def _to_native(x: Any)\
        -> Any:
    if isinstance(x, ivy.Array):
        return _to_native(x.data)
    elif isinstance(x, ivy.Container):
        return x.to_native()
    return x


def _to_ivy(x: Any)\
        -> Any:
    if isinstance(x, (ivy.Array, ivy.Variable)):
        return x
    elif isinstance(x, ivy.Container):
        return x.to_ivy()
    return ivy.Variable(x) if ivy.is_variable(x, exclusive=True) else ivy.Array(x) if ivy.is_native_array(x) else x


# Wrapped #
# --------#

def to_ivy(x: Union[Union[ivy.Array, ivy.NativeArray], Iterable],
           nested: bool = False,
           include_derived: bool = False)\
        -> Union[Union[ivy.Array, ivy.NativeArray], Iterable]:
    """
    Returns the input array converted to an ivy.Array instances if it is an array type, otherwise the input is
    returned unchanged. If nested is set, the check is applied to all nested leafs of tuples,
    lists and dicts contained within x.

    :param x: The input to maybe convert.
    :type x: any
    :param nested: Whether to apply the conversion on arguments in a nested manner. If so, all dicts, lists and
                   tuples will be traversed to their lowest leaves in search of ivy.Array and ivy.Variable instances.
                   Default is False.
    :type nested: bool, optional
    :param include_derived: Whether to also recursive for classes derived from tuple, list and dict. Default is False.
    :type include_derived: bool, optional
    :return: the input in it's native framework form in the case of ivy.Array or ivy.Variable instances.
    """
    if nested:
        return ivy.nested_map(x, _to_ivy, include_derived)
    return _to_ivy(x)


def args_to_ivy(*args: Iterable[Any],
                include_derived: bool = False,
                **kwargs: Dict[str, Any])\
        -> Tuple[Iterable[Any], Dict[str, Any]]:
    """
    Returns args and keyword args in their ivy.Array or ivy.Variable form for all nested instances,
    otherwise the arguments are returned unchanged.

    :param args: The positional arguments to check
    :type args: sequence of arguments
    :param include_derived: Whether to also recursive for classes derived from tuple, list and dict. Default is False.
    :type include_derived: bool, optional
    :param kwargs: The key-word arguments to check
    :type kwargs: dict of arguments
    :return: the same arguments, with any nested arrays converted to ivy.Array or ivy.Variable instances.
    """
    native_args = ivy.nested_map(args, _to_ivy, include_derived)
    native_kwargs = ivy.nested_map(kwargs, _to_ivy, include_derived)
    return native_args, native_kwargs


def to_native(x: Union[Union[ivy.Array, ivy.NativeArray], Iterable],
              nested: bool = False,
              include_derived: bool = False)\
        -> Union[Union[ivy.Array, ivy.NativeArray], Iterable]:
    """
    Returns the input item in it's native backend framework form if it is an ivy.Array or ivy.Variable instance.
    otherwise the input is returned unchanged. If nested is set, the check is applied to all nested leafs of tuples,
    lists and dicts contained within x.

    :param x: The input to maybe convert.
    :type x: any
    :param nested: Whether to apply the conversion on arguments in a nested manner. If so, all dicts, lists and
                   tuples will be traversed to their lowest leaves in search of ivy.Array and ivy.Variable instances.
                   Default is False.
    :type nested: bool, optional
    :param include_derived: Whether to also recursive for classes derived from tuple, list and dict. Default is False.
    :type include_derived: bool, optional
    :return: the input in it's native framework form in the case of ivy.Array or ivy.Variable instances.
    """
    if nested:
        return ivy.nested_map(x, _to_native, include_derived)
    return _to_native(x)


def args_to_native(*args: Iterable[Any],
                   include_derived: bool = False,
                   **kwargs: Dict[str, Any],
                   )\
        -> Tuple[Iterable[Any], Dict[str, Any]]:
    """
    Returns args and keyword args in their native backend framework form for all nested ivy.Array or ivy.Variable
    instances, otherwise the arguments are returned unchanged.
    :param args: The positional arguments to check
    :type args: sequence of arguments
    :param include_derived: Whether to also recursive for classes derived from tuple, list and dict. Default is False.
    :type include_derived: bool, optional
    :param kwargs: The key-word arguments to check
    :type kwargs: dict of arguments
    :return: the same arguments, with any nested ivy.Array or ivy.Variable instances converted to their native form.
    """
    native_args = ivy.nested_map(args, _to_native, include_derived)
    native_kwargs = ivy.nested_map(kwargs, _to_native, include_derived)
    return native_args, native_kwargs
