"""Collection of image Ivy functions."""

# local
import ivy as ivy
import numpy as _np
from ivy.framework_handler import current_framework as _cur_framework
from typing import Union, List, Tuple, Optional


# Extra #
# ------#


def stack_images(
    images: List[Union[ivy.Array, ivy.Array, ivy.NativeArray]],
    desired_aspect_ratio: Tuple[int, int] = (1, 1),
) -> ivy.Array:
    """Stacks a group of images into a combined windowed image, fitting the desired
    aspect ratio as closely as possible.

    Parameters
    ----------
    images
        Sequence of image arrays to be stacked *[batch_shape,height,width,dims]*
    desired_aspect_ratio:
        desired aspect ratio of the stacked image

    Returns
    -------
    ret
        an array containing the stacked images in a specified aspect ratio/dimensions

    Examples
    --------
    >>> import ivy
    >>> shape, num = (1, 2, 3), 2
    >>> data = [ivy.ones(shape)] * num
    >>> stacked = ivy.stack_images(data, (2, 1))
    >>> print(stacked)
    [[[1., 1., 1.],
            [1., 1., 1.],
            [0., 0., 0.],
            [0., 0., 0.]],

           [[1., 1., 1.],
            [1., 1., 1.],
            [0., 0., 0.],
            [0., 0., 0.]]]

    """
    return _cur_framework(images[0]).stack_images(images, desired_aspect_ratio)


def bilinear_resample(x, warp):
    """Performs bilinearly re-sampling on input image.

    Parameters
    ----------
    x
        Input image *[batch_shape,h,w,dims]*.
    warp
        Warp array *[batch_shape,num_samples,2]*

    Returns
    -------
    ret
        Image after bilinear re-sampling.

    """
    return _cur_framework(x).bilinear_resample(x, warp)


def gradient_image(x):
    """Computes image gradients (dy, dx) for each channel.

    Parameters
    ----------
    x
        Input image *[batch_shape, h, w, d]* .

    Returns
    -------
    ret
        Gradient images dy *[batch_shape,h,w,d]* and dx *[batch_shape,h,w,d]* .

    Examples
    --------
    >>> batch_size = 1
    >>> h = 3
    >>> w = 3
    >>> d = 1
    >>> x = ivy.arange(h * w * d, dtype=ivy.float32)
    >>> image = ivy.reshape(x,shape=(batch_size, h, w, d))
    >>> dy, dx = ivy.gradient_image(image)
    >>> print(image[0, :,:,0])
    ivy.array([[0., 1., 2.],
               [3., 4., 5.],
               [6., 7., 8.]])
    >>> print(dy[0, :,:,0])
     ivy.array([[3., 3., 3.],
               [3., 3., 3.],
               [0., 0., 0.]])
    >>> print(dx[0, :,:,0])
     ivy.array([[1., 1., 0.],
               [1., 1., 0.],
               [1., 1., 0.]])

    """
    return _cur_framework(x).gradient_image(x)


def float_img_to_uint8_img(x):
    """Converts an image of floats into a bit-cast 4-channel image of uint8s, which can
    be saved to disk.

    Parameters
    ----------
    x
        Input float image *[batch_shape,h,w]*.

    Returns
    -------
    ret
        The new encoded uint8 image *[batch_shape,h,w,4]* .

    """
    x_np = ivy.to_numpy(x)
    x_shape = x_np.shape
    x_bytes = x_np.tobytes()
    x_uint8 = _np.frombuffer(x_bytes, _np.uint8)
    return ivy.array(_np.reshape(x_uint8, list(x_shape) + [4]).tolist())


def uint8_img_to_float_img(x):
    """Converts an image of uint8 values into a bit-cast float image.

    Parameters
    ----------
    x
        Input uint8 image *[batch_shape,h,w,4]*.

    Returns
    -------
    ret
        The new float image *[batch_shape,h,w]*

    """
    x_np = ivy.to_numpy(x)
    x_shape = x_np.shape
    x_bytes = x_np.tobytes()
    x_float = _np.frombuffer(x_bytes, _np.float32)
    return ivy.array(_np.reshape(x_float, x_shape[:-1]).tolist())


def random_crop(
    x: Union[ivy.Array, ivy.NativeArray], 
    crop_size: Tuple[int, int], 
    batch_shape: Optional[List[int]] = None, 
    image_dims: Optional[List[int]] = None
) -> ivy.Array:
    """Randomly crops the input images according to the provided crop size.

    Parameters
    ----------
    x
        Input images to crop *[batch_shape,h,w,f]*
    crop_size
        The 2D crop size *[cs_h, cs_w]*
    batch_shape
        Shape of batch. Inferred from inputs if None. (Default value = None)
    image_dims
        Image dimensions. Inferred from inputs in None. (Default value = None)

    Returns
    -------
    ret
        An array containing the cropped image of shape *[batch_shape, cs_h, cs_w, f]*

    Examples
    --------
    >>> batch_size, h, w, f = 1, 3, 3, 1
    >>> x = ivy.arange(batch_size * h * w * f, dtype=ivy.float32)
    >>> x = ivy.reshape(x, shape=(batch_size, h, w, f))
    >>> cropped_output = ivy.random_crop(x, (2,2))
    >>> print(x[0, :, :, 0])
    ivy.array([[0., 1., 2.],
               [3., 4., 5.],
               [6., 7., 8.]])
    >>> print(cropped_output[0, :, :, 0])
    ivy.array([[3., 4.],
               [6., 7.]])

    """

    return _cur_framework(x).random_crop(x, crop_size, batch_shape, image_dims)


def linear_resample(
    x: Union[ivy.Array, ivy.NativeArray], num_samples: int, axis: int = -1
) -> Union[ivy.Array, ivy.NativeArray]:
    """Performs linear re-sampling on input image.

    Parameters
    ----------
    x
        Input array
    num_samples
        The number of interpolated samples to take.
    axis
        The axis along which to perform the resample. Default is last dimension.

    Returns
    -------
    ret
        The array after the linear resampling.

    """
    return _cur_framework(x).linear_resample(x, num_samples, axis)
