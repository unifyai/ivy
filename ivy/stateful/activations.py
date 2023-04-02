"""Collection of Ivy neural network activations as stateful classes."""

# local
import ivy
from ivy.stateful.module import Module


class GELU(Module):
    def __init__(self, *, approximate: bool = False):
        """Applies the GELU activation function."""
        self._approximate = approximate
        Module.__init__(self)

    def _forward(self, x, /, *, approximate=None):
        """
        Perform forward pass of the GELU activation.

        Parameters
        ----------
        x
            Inputs to process *[batch_shape, d]*.

        Returns
        -------
        ret
            The outputs following the GELU activation *[batch_shape, d]*
        """
        return ivy.gelu(x, approximate=ivy.default(approximate, self._approximate))


class GEGLU(Module):
    def __init__(self):
        """Applies the GEGLU activation function."""
        Module.__init__(self)

    def _forward(self, inputs):
        """
        Perform forward pass of the GEGLU activation.

        Parameters
        ----------
        inputs
            Inputs to process *[batch_shape, 2d]*.

        Returns
        -------
        ret
            The outputs following the GEGLU activation *[batch_shape, d]*

        """
        x, gates = ivy.split(inputs, num_or_size_splits=2, axis=-1)
        return ivy.gelu(gates) * x


class RELU(Module):
    def __init__(self):
        """
        Applies the RELU activation function
        """
        Module.__init__(self)

    def _forward(self, x):
        """

        Parameters
        ----------
        x
            Inputs to process *[batch_shape, d]*.
        Returns
        -------
        ret
            The outputs following the RELU activation *[batch_shape, d]*
        """

        return ivy.relu(x)


class LRELU(Module):
    def __init__(self, alpha: float = 0.2):
        """
        Applies the LEAKY RELU activation function
        Parameters
        ----------
        alpha
             Negative slope for ReLU.
        """
        self._alpha = alpha
        Module.__init__()

    def _forward(self, x, *, alpha=None):
        """

        Parameters
        ----------
        x
              Inputs to process *[batch_shape, d]*.
        alpha
              Negative slope for ReLU.

        Returns
        -------
        ret
            The outputs following the LEAKY RELU activation *[batch_shape, d]*
        """
        return ivy.leaky_relu(x, alpha=ivy.default(alpha, self._alpha))


class LOG_SOFTMAX(Module):
    def __init__(self):
        """
        Applies the LOG SOFTMAX activation function
        """
        Module.__init__(self)

    def _forward(self, x, *, axis=None):
        """

        Parameters
        ----------
        x
            Inputs to process *[batch_shape, d]*.
        axis
            The dimension log_softmax would be performed on. The default is ``None``
        Returns
        -------
         ret
            The outputs following the LOG SOFTMAX activation *[batch_shape, d]*
        """
        return ivy.log_softmax(x, axis=axis)


class SOFTMAX(Module):
    def __init__(self):
        """
        Applies the SOFTMAX activation function
        """
        Module.__init__(self)

    def _forward(self, x, *, axis=None):
        """

        Parameters
        ----------
        x
            Inputs to process *[batch_shape, d]*.
        axis
            The dimension softmax would be performed on. The default is ``None``.
        Returns
        -------
          ret
            The outputs following the SOFTMAX activation *[batch_shape, d]*

        """
        return ivy.softmax(x, axis)


class SOFTPLUS(Module):
    def __init__(self):
        """
        Applies the SOFTPLUS activation function
        """
        Module.__init__(self)

    def _forward(self, x, *, beta=None, threshold=None):
        """

        Parameters
        ----------
        x
            Inputs to process *[batch_shape, d]*.
        beta
            The beta value for the softplus formation. Default: ``None``.

        threshold
             values above this revert to a linear function. Default: ``None``.

        Returns
        -------
        ret
            The outputs following the SOFTPLUS activation *[batch_shape, d]*

        """
        return ivy.softplus(x, beta=beta, threshold=threshold)


class MISH(Module):
    def __init__(self):
        """
        Applies the MISH activation function
        """
        Module.__init__(self)

    def _forward(self, x):
        """

        Parameters
        ----------
        x
             Inputs to process *[batch_shape, d]*.

        Returns
        -------
         ret
            The outputs following the MISH activation *[batch_shape, d]*
        """
        return ivy.mish(x)
