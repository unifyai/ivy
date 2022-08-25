# global
import ivy


def expm1(
    x,
    /,
    out=None,
    *,
    dtype=None,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.expm1(x, out=out)
    return ret


def exp2(
    x,
    /,
    out=None,
    *,
    dtype=None,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.pow(2, x, out=out)
    return ret


def log10(
    x,
    /,
    out=None,
    *,
    dtype=None,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.log10(x, out=out)
    return ret


def log2(
    x,
    /,
    out=None,
    *,
    dtype=None,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.log2(x, out=out)
    return ret


def log1p(
    x,
    /,
    out=None,
    *,
    dtype=None,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.log1p(x, out=out)
    return ret


def logaddexp(
    x1,
    x2,
    /,
    out=None,
    *,
    dtype=None,
):
    if dtype:
        x1 = ivy.astype(ivy.array(x1), ivy.as_ivy_dtype(dtype))
        x2 = ivy.astype(ivy.array(x2), ivy.as_ivy_dtype(dtype))
    ret = ivy.logaddexp(x1, x2, out=out)
    return ret
