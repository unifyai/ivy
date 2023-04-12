import ivy
from ivy.functional.frontends.numpy.func_wrapper import to_ivy_arrays_and_back



@to_ivy_arrays_and_back
def ifft(a, n=None, axis=-1, norm=None):
    a = ivy.array(a, dtype=ivy.complex128)
    if norm is None:
        norm = "backward"
    return ivy.ifft(a, axis, norm=norm, n=n)


@to_ivy_arrays_and_back
def ifftshift(x, axes=None):
    # The inverse of `fftshift`. Although identical for even-length `x`, the
    # functions differ by one sample for odd-length `x`.

    # Parameters
    # ----------
    # x : array_like
    #     Input array.
    # axes : int or shape tuple, optional
    #     Axes over which to calculate.  Defaults to None, which shifts all axes.

    # Returns
    # -------
    # y : ndarray
    #     The shifted array.

    x = ivy.asarray(x)
    if axes is None:
        axes = tuple(range(x.ndim))
        shift = [-(dim // 2) for dim in x.shape]
    elif isinstance(axes, (int, ivy.uint8, ivy.uint16, ivy.uint32, ivy.uint64)):
        shift = -(x.shape[axes] // 2)
    else:
        shift = [-(x.shape[ax] // 2) for ax in axes]

    return ivy.roll(x, shift, axes)
