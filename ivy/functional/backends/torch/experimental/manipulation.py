# global
from typing import Optional, Union, Sequence, Tuple, NamedTuple, List, Literal, Callable, Any
from numbers import Number
from collections import namedtuple
import torch

# local
import numpy as np
from ivy.func_wrapper import with_unsupported_dtypes
from .. import backend_version
import ivy


def moveaxis(
    a: torch.Tensor,
    source: Union[int, Sequence[int]],
    destination: Union[int, Sequence[int]],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if copy:
        a = torch.clone(a)
    return torch.moveaxis(a, source, destination)


moveaxis.support_native_out = False


def heaviside(
    x1: torch.tensor,
    x2: torch.tensor,
    /,
    *,
    out: Optional[torch.tensor] = None,
) -> torch.tensor:
    return torch.heaviside(
        x1,
        x2,
        out=out,
    )


heaviside.support_native_out = True


def flipud(
    m: torch.Tensor,
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[torch.tensor] = None,
) -> torch.tensor:
    if copy:
        m = torch.clone(m)
    return torch.flipud(m)


flipud.support_native_out = False


def vstack(
    arrays: Sequence[torch.Tensor],
    /,
    *,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if not isinstance(arrays, tuple):
        arrays = tuple(arrays)
    return torch.vstack(arrays, out=None)


def hstack(
    arrays: Sequence[torch.Tensor],
    /,
    *,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if not isinstance(arrays, tuple):
        arrays = tuple(arrays)
    return torch.hstack(arrays, out=None)


def rot90(
    m: torch.Tensor,
    /,
    *,
    copy: Optional[bool] = None,
    k: int = 1,
    axes: Tuple[int, int] = (0, 1),
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if copy:
        m = torch.clone(m)
    return torch.rot90(m, k, axes)


def top_k(
    x: torch.Tensor,
    k: int,
    /,
    *,
    axis: int = -1,
    largest: bool = True,
    sorted: bool = True,
    out: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
) -> Tuple[torch.Tensor, torch.Tensor]:
    k = min(k, x.shape[axis])
    topk_res = NamedTuple(
        "top_k", [("values", torch.Tensor), ("indices", torch.Tensor)]
    )
    if not largest:
        indices = torch.argsort(x, dim=axis)
        indices = torch.index_select(indices, axis, torch.arange(k))
    else:
        indices = torch.argsort(-x, dim=axis)
        indices = torch.index_select(indices, axis, torch.arange(k))
    if not sorted:
        indices = torch.sort(indices, dim=axis)[0]
    val = torch.gather(x, axis, indices)
    return topk_res(val, indices)


def fliplr(
    m: torch.Tensor,
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[torch.tensor] = None,
) -> torch.tensor:
    if copy:
        m = torch.clone(m)
    return torch.fliplr(m)


fliplr.support_native_out = False


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def i0(
    x: torch.Tensor,
    /,
    *,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.i0(x, out=out)


i0.support_native_out = True


def flatten(
    x: torch.Tensor,
    /,
    *,
    copy: bool = None,
    start_dim: int = 0,
    end_dim: int = -1,
    order: str = "C",
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    ivy.utils.assertions.check_elem_in_list(order, ["C", "F"])
    if copy:
        x = torch.clone(x)
    if order == "F":
        return ivy.functional.experimental.flatten(
            x, start_dim=start_dim, end_dim=end_dim, order=order
        )
    return torch.flatten(x, start_dim=start_dim, end_dim=end_dim)


def vsplit(
    ary: torch.Tensor,
    indices_or_sections: Union[int, Tuple[int, ...]],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[torch.Tensor]:
    if copy:
        ary = torch.clone(ary)
    return torch.vsplit(ary, indices_or_sections)


def dsplit(
    ary: torch.Tensor,
    indices_or_sections: Union[int, Tuple[int, ...]],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[torch.Tensor]:
    if len(ary.shape) < 3:
        raise ivy.utils.exceptions.IvyError(
            "dsplit only works on arrays of 3 or more dimensions"
        )
    if copy:
        ary = torch.clone(ary)
    return list(torch.dsplit(ary, indices_or_sections))


def atleast_1d(*arys: torch.Tensor, copy: Optional[bool] = None) -> List[torch.Tensor]:
    if copy:
        arys = ivy.nested_map(arys, torch.clone)
    transformed = torch.atleast_1d(*arys)
    if isinstance(transformed, tuple):
        return list(transformed)
    return transformed


def dstack(
    arrays: Sequence[torch.Tensor],
    /,
    *,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if not isinstance(arrays, tuple):
        arrays = tuple(arrays)
    return torch.dstack(arrays, out=out)


def atleast_2d(*arys: torch.Tensor, copy: Optional[bool] = None) -> List[torch.Tensor]:
    if copy:
        arys = ivy.nested_map(arys, torch.clone)
    transformed = torch.atleast_2d(*arys)
    if isinstance(transformed, tuple):
        return list(transformed)
    return transformed


def atleast_3d(
    *arys: Union[torch.Tensor, bool, Number], copy: Optional[bool] = None
) -> List[torch.Tensor]:
    if copy:
        arys = ivy.nested_map(arys, torch.clone)
    transformed = torch.atleast_3d(*arys)
    if isinstance(transformed, tuple):
        return list(transformed)
    return transformed


@with_unsupported_dtypes({"2.0.1 and below": ("float16", "bfloat16")}, backend_version)
def take_along_axis(
    arr: torch.Tensor,
    indices: torch.Tensor,
    axis: int,
    /,
    *,
    mode: str = "fill",
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if arr.ndim != indices.ndim:
        raise ivy.utils.exceptions.IvyException(
            "arr and indices must have the same number of dimensions;"
            + f" got {arr.ndim} vs {indices.ndim}"
        )
    indices = indices.long()
    if mode not in ["clip", "fill", "drop"]:
        raise ValueError(
            f"Invalid mode '{mode}'. Valid modes are 'clip', 'fill', 'drop'."
        )
    arr_shape = arr.shape
    if axis < 0:
        axis += arr.ndim
    if mode == "clip":
        max_index = arr.shape[axis] - 1
        indices = torch.clamp(indices, 0, max_index)
    elif mode == "fill" or mode == "drop":
        if "float" in str(arr.dtype):
            fill_value = float("nan")
        elif "uint" in str(arr.dtype):
            fill_value = torch.iinfo(arr.dtype).max
        else:
            fill_value = -torch.iinfo(arr.dtype).max - 1
        indices = torch.where((indices < 0) | (indices >= arr.shape[axis]), -1, indices)
        arr_shape = list(arr_shape)
        arr_shape[axis] = 1
        fill_arr = torch.full(arr_shape, fill_value, dtype=arr.dtype)
        arr = torch.cat([arr, fill_arr], dim=axis)
        indices = torch.where(indices < 0, arr.shape[axis] + indices, indices)
    return torch.take_along_dim(arr, indices, axis, out=out)


def hsplit(
    ary: torch.Tensor,
    indices_or_sections: Union[int, Tuple[int, ...]],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[torch.Tensor]:
    if copy:
        ary = torch.clone(ary)
    return list(torch.hsplit(ary, indices_or_sections))


take_along_axis.support_native_out = True


def broadcast_shapes(*shapes: Union[List[int], List[Tuple]]) -> Tuple[int]:
    return tuple(torch.broadcast_shapes(*shapes))


broadcast_shapes.support_native_out = False


def expand(
    x: torch.Tensor,
    shape: Union[List[int], List[Tuple]],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if copy:
        x = torch.clone(x)
    return x.expand(shape)


expand.support_native_out = False


def concat_from_sequence(
    input_sequence: Union[Tuple[torch.Tensor], List[torch.Tensor]],
    /,
    *,
    new_axis: int = 0,
    axis: int = 0,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    is_tuple = type(input_sequence) is tuple
    if is_tuple:
        input_sequence = list(input_sequence)
    if new_axis == 0:
        ret = torch.cat(input_sequence, dim=axis)
        return ret
    elif new_axis == 1:
        ret = torch.stack(input_sequence, dim=axis)
        return ret


@with_unsupported_dtypes({"2.0.1 and below": ("complex", "float16")}, backend_version)
def unique_consecutive(
    x: torch.Tensor,
    /,
    *,
    axis: Optional[int] = None,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    Results = namedtuple(
        "Results",
        ["output", "inverse_indices", "counts"],
    )
    output, inverse_indices, counts = torch.unique_consecutive(
        x,
        return_inverse=True,
        return_counts=True,
        dim=axis,
    )
    return Results(
        output.to(x.dtype),
        inverse_indices,
        counts,
    )
  
  
def _can_handle_padding(input, pad, mode):

    # if it is not tuple of integers then convert it
    if all(isinstance(sub_tuple, tuple) for sub_tuple in pad):
        pad = tuple(element for sub_tuple in pad for element in sub_tuple)

    if not isinstance(pad, tuple) or len(pad) % 2 != 0 or len(pad) < 2 or len(pad) > 6:
        return False

    if input.dim() < 2 or input.dim() > 5:
        return False

    if mode in ['reflect', 'replicate']:
        if input.dim() == 2 and len(pad) > 2:
            return False
        if input.dim() == 3 and len(pad) > 4:
            return False
        if input.dim() == 4 and len(pad) < 4:
            return False
        if input.dim() == 5 and len(pad) < 6:
            return False

            # reflect padding requires that padding size is less than input size for each dim
        if mode == 'reflect':
            for i in range(-1, -len(pad) - 1, -2):
                if pad[i] >= input.size(i // 2):
                    return False
                if pad[i - 1] >= input.size(i // 2):
                    return False

    if mode == 'circular':
        if input.dim() < 3:
            return False
        if input.dim() == 3 and len(pad) != 2:
            return False
        if input.dim() == 4 and len(pad) != 4:
            return False
        if input.dim() == 5 and len(pad) != 6:
            return False

            # circular padding requires that padding size is less than input size for last dim
        if pad[-1] > input.size(-1) or pad[-2] > input.size(-1):
            return False

    return True


def _check_tuple(t):
    if isinstance(t, tuple):
        if len(t) == 1 and not isinstance(t[0], tuple):
            return t[0], True
        else:
            has_multiple_values = False
            size = 0
            for elem in t:
                elem_val, elem_has_multiple_values = _check_tuple(elem)
                if elem_has_multiple_values:
                    has_multiple_values = True
                size += elem_val
            return size, has_multiple_values
    else:
        return 1, False


def _check(*args, **kwargs):

    mode = kwargs['mode']
    if mode in ["linear_ramp",
                    "maximum",
                    "symmetric",
                    "mean",
                    "median",
                    "minimum",
                    "edge",
                    "wrap",
                    "empty",
    ]:
        return False
    else:
        inp = args[0]
        pad = args[1]
        if mode == 'constant':

            c = kwargs['constant_values']
            val, cond = _check_tuple(c)
            if cond is False:
                return False
            else:
                kwargs['constant_values'] = val
                return True
        elif _can_handle_padding(inp.shape, pad, mode):
            return True
        else:
	   if kwargs['mode'] == 'replicate':
                kwargs['mode'] = 'edge'
            elif kwargs['mode'] == 'circular':
                kwargs['mode'] = 'wrap'
            return False


@with_unsupported_dtypes({"1.11.0 and below": ("float16", "bfloat16", "complex64", "complex128")}, backend_version)
def pad(
    input: torch.Tensor,
    pad_width: Union[Sequence[Sequence[int]], torch.Tensor, int],
    /,
    *,
    mode: Union[
        Literal[
            "constant",
            "edge",
            "reflect",
            "wrap",
        ],
        Callable,
    ] = "constant",
    stat_length: Union[Sequence[torch.Tensor], int] = 1,
    constant_values: Number = 0,
    end_values: Number = 0,
    reflect_type: Literal["even", "odd"] = "even",
    **kwargs: Optional[Any],
) -> torch.Tensor:

    return torch.nn.functional.pad(
        input=input,
        pad=pad_width,
        mode=mode,
        value=constant_values,
        )


pad.partial_mixed_handler = lambda *args, **kwargs: _check(*args, **kwargs)
