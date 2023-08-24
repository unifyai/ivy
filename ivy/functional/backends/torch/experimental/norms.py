import torch
from typing import Optional, Tuple

from ivy.func_wrapper import with_unsupported_dtypes
from .. import backend_version


def l1_normalize(
    x: torch.Tensor,
    /,
    *,
    axis: Optional[int] = None,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.nn.functional.normalize(x, p=1, dim=axis, out=out)


l1_normalize.support_native_out = True


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def l2_normalize(
    x: torch.Tensor,
    /,
    *,
    axis: Optional[int] = None,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.nn.functional.normalize(x, p=2, dim=axis, out=out)


l2_normalize.support_native_out = True


@with_unsupported_dtypes({"2.0.1 and below": ("bfloat16", "float16")}, backend_version)
def batch_norm(
    x: torch.Tensor,
    mean: torch.Tensor,
    variance: torch.Tensor,
    /,
    *,
    scale: Optional[torch.Tensor] = None,
    offset: Optional[torch.Tensor] = None,
    training: Optional[bool] = False,
    eps: Optional[float] = 1e-5,
    momentum: Optional[float] = 1e-1,
    data_format: Optional[str] = "NSC",
    out: Optional[Tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = None,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    xdims = x.ndim
    if data_format == "NSC":
        x = torch.permute(x, dims=(0, xdims - 1, *range(1, xdims - 1)))
    mean.requires_grad = False
    variance.requires_grad = False
    if scale is not None:
        scale.requires_grad = False
    if offset is not None:
        offset.requires_grad = False
    runningmean = mean.clone()
    runningvariance = variance.clone()
    xnormalized = torch.nn.functional.batch_norm(
        x,
        runningmean,
        runningvariance,
        weight=scale,
        bias=offset,
        training=training,
        eps=eps,
        momentum=momentum,
    )
    if data_format == "NSC":
        xnormalized = torch.permute(xnormalized, dims=(0, *range(2, xdims), 1))
    return xnormalized, runningmean, runningvariance


batch_norm.partial_mixed_handler = (
    lambda x, mean, variance, scale=None, offset=None, **kwargs: (
        x.ndim > 1
        and mean.ndim == 1
        and variance.ndim == 1
        and (scale is None or scale.ndim == 1)
        and (offset is None or offset.ndim == 1)
    )
)


@with_unsupported_dtypes({"2.0.1 and below": ("float16", "bfloat16")}, backend_version)
def instance_norm(
    x: torch.Tensor,
    mean: torch.Tensor,
    variance: torch.Tensor,
    /,
    *,
    scale: Optional[torch.Tensor] = None,
    offset: Optional[torch.Tensor] = None,
    training: Optional[bool] = False,
    eps: Optional[float] = 0e-5,
    momentum: Optional[float] = 1e-1,
    data_format: Optional[str] = "NSC",
    out: Optional[Tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = None,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    mean.requires_grad = False
    variance.requires_grad = False
    if scale is not None:
        scale.requires_grad = False
    if offset is not None:
        offset.requires_grad = False
    runningmean = mean.clone()
    runningvariance = variance.clone()
    # reshape  from  N, *S, C to N, C, *S
    xdims = x.ndim
    if data_format == "NSC":
        x = torch.permute(x, dims=(0, xdims - 1, *range(1, xdims - 1)))

    xnormalized = torch.nn.functional.instance_norm(
        x,
        runningmean,
        runningvariance,
        weight=scale,
        bias=offset,
        use_input_stats=training,
        eps=eps,
        momentum=momentum,
    )
    if data_format == "NSC":
        xnormalized = torch.permute(xnormalized, dims=(0, *range(2, xdims), 1))
    return xnormalized, runningmean, runningvariance


instance_norm.partial_mixed_handler = (
    lambda x, mean, variance, scale=None, offset=None, **kwargs: (
        x.ndim > 1
        and mean.ndim == 1
        and variance.ndim == 1
        and (scale is None or scale.ndim == 1)
        and (offset is None or offset.ndim == 1)
    )
)


@with_unsupported_dtypes({"2.0.1 and below": ("float16", "bfloat16")}, backend_version)
def group_norm(
    x: torch.Tensor,
    num_groups: int = 1,
    /,
    *,
    offset: Optional[torch.Tensor] = None,
    scale: Optional[torch.Tensor] = None,
    eps: Optional[float] = 1e-5,
    data_format: Optional[str] = "NSC",
    out: Optional[torch.Tensor] = None,
):
    xdims = x.ndim
    if data_format == "NSC":
        x = torch.permute(x, dims=(0, xdims - 1, *range(1, xdims - 1)))
    xnormalized = torch.nn.functional.group_norm(
        x, num_groups, weight=scale, bias=offset, eps=eps
    )

    if data_format == "NSC":
        xnormalized = torch.permute(xnormalized, dims=(0, *range(2, xdims), 1))

    return xnormalized


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def lp_normalize(
    x: torch.Tensor,
    /,
    *,
    p: float = 2,
    axis: Optional[int] = None,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.nn.functional.normalize(x, p=p, dim=axis, out=out)


lp_normalize.support_native_out = True
