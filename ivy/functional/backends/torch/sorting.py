# global
import torch
from typing import Optional

# local
import ivy


def argsort(
    x: torch.Tensor,
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if out is not None:
        out = tuple([torch.zeros(x.shape, dtype=x.dtype), out.long()])
    _, sorted_indices = torch.sort(
        x, dim=axis, descending=descending, stable=stable, out=out
    )
    return sorted_indices


argsort.support_native_out = True


def sort(
    x: torch.Tensor,
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if out is not None:
        out = tuple([out, torch.zeros(out.shape, dtype=torch.long)])
    sorted_tensor, _ = torch.sort(
        x, dim=axis, descending=descending, stable=stable, out=out
    )
    return sorted_tensor


sort.support_native_out = True


def searchsorted(
    x: torch.Tensor,
    v: torch.Tensor,
    /,
    *,
    side="left",
    sorter=None,
    ret_dtype=torch.int64,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    assert ivy.is_int_dtype(ret_dtype), ValueError(
        "only Integer data types are supported for ret_dtype."
    )
    if sorter is not None:
        sorter_dtype = ivy.as_native_dtype(sorter.dtype)
        assert ivy.is_int_dtype(sorter_dtype) and not ivy.is_uint_dtype(
            sorter_dtype
        ), TypeError(
            f"Only signed integer data type for sorter is allowed, got {sorter_dtype }."
        )
        sorter = sorter.to(torch.int64)
    ret_dtype = ivy.as_native_dtype(ret_dtype)
    func_out = out
    if ivy.exists(out) and out.dtype != ret_dtype:
        func_out = None
    if ret_dtype is torch.int64:
        return torch.searchsorted(
            x,
            v,
            sorter=sorter,
            side=side,
            out_int32=False,
            out=func_out,
        )
    elif ret_dtype is torch.int32:
        return torch.searchsorted(
            x,
            v,
            sorter=sorter,
            side=side,
            out_int32=True,
            out=func_out,
        )
    if ivy.exists(out):
        return ivy.inplace_update(
            out, torch.searchsorted(x, v, sorter=sorter, side=side).to(out.dtype)
        )
    return torch.searchsorted(x, v, sorter=sorter, side=side).to(ret_dtype)


searchsorted.support_native_out = True
