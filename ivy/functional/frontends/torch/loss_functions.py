# global
import ivy


def _get_reduction_func(reduction):
    if reduction == "none":
        ret = lambda x: x
    elif reduction == "mean":
        ret = ivy.mean
    elif reduction == "sum":
        ret = ivy.sum
    else:
        raise ivy.exceptions.IvyException(
            "{} is not a valid value for reduction".format(reduction)
        )
    return ret


def _legacy_get_string(size_average, reduce):
    if size_average is None:
        size_average = True
    if reduce is None:
        reduce = True
    if size_average and reduce:
        ret = "mean"
    elif reduce:
        ret = "sum"
    else:
        ret = "none"
    return ret


def _get_reduction(reduction, size_average=None, reduce=None):
    if size_average is not None or reduce is not None:
        return _get_reduction_func(_legacy_get_string(size_average, reduce))
    else:
        return _get_reduction_func(reduction)


def _get_reduction_method(reduction, to_reduce):
    if reduction == "none":
        ret = to_reduce
    elif reduction == "mean":
        ret = ivy.mean(to_reduce)
    elif reduction == "sum":
        ret = ivy.sum(to_reduce)
    else:
        raise ivy.exceptions.IvyException(
            f"{reduction} is not a valid value for reduction"
        )
    return ret


def _get_reduction_string(size_average, reduce):
    if size_average is None:
        size_average = True
    if reduce is None:
        reduce = True
    if size_average and reduce:
        ret = "mean"
    elif reduce:
        ret = "sum"
    else:
        ret = "none"
    return ret


def _apply_reduction(reduction, size_average, reduce, to_reduce):
    if size_average is not None or reduce is not None:
        reduction = _get_reduction_string(size_average, reduce)
        return _get_reduction_method(reduction, to_reduce)
    else:
        return _get_reduction_method(reduction, to_reduce)


def cross_entropy(
    input,
    target,
    weight=None,
    size_average=None,
    ignore_index=-100,
    reduce=None,
    reduction="mean",
    label_smoothing=0.0,
):
    input = ivy.softmax(input)
    ret = ivy.cross_entropy(target, input, epsilon=label_smoothing)
    if weight is not None:
        ret = ivy.multiply(weight, ret)
    ret = _apply_reduction(reduction, size_average, reduce, ret)
    return ret


def binary_cross_entropy(
    input, target, weight=None, size_average=None, reduce=None, reduction="mean"
):
    reduction = _get_reduction(reduction, size_average, reduce)
    result = ivy.binary_cross_entropy(target, input, epsilon=0.0)

    if weight is not None:
        result = ivy.multiply(weight, result)
    result = reduction(result)
    return result


def triplet_margin_loss(
    anchor,
    positive,
    negative,
    margin=1.0,
    p=2,
    eps=1e-06,
    swap=False,
    size_average=None,
    reduce=None,
    reduction="mean",
):
    delta_plus = ivy.vector_norm(anchor - positive + eps, ord=p, axis=-1)
    delta_minus = ivy.vector_norm(anchor - negative + eps, ord=p, axis=-1)
    if swap:
        delta_minus = ivy.minimum(
            delta_minus,
            ivy.vector_norm(positive - negative + eps, ord=p, axis=-1),
        )
    ret = ivy.maximum(delta_plus - delta_minus + margin, 0)
    ret = _apply_reduction(reduction, size_average, reduce, ret)
    return ret


triplet_margin_loss.unsupported_dtypes = ("float16", "bloat16")
