"""
Collection of random Ivy functions
"""

# local
from ivy.framework_handler import current_framework as _cur_framework


# Extra #
# ------#

def random_uniform(low=0.0, high=1.0, shape=None, dev=None):
    """Draws samples from a uniform distribution.
    Samples are uniformly distributed over the half-open interval [low, high) (includes low, but excludes high).
    In other words, any value within the given interval is equally likely to be drawn by uniform.

    Parameters
    ----------
    low : float
        Lower boundary of the output interval. All values generated will be greater than or equal to low.
        The default value is 0.
    high : float
        Upper boundary of the output interval. All values generated will be less than high.
        The default value is 1.0.
    shape : sequence of ints
        Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn.
        If size is None (default), a single value is returned.
    dev : ivy.Device
        device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc. (Default value = None)

    Returns
    -------
    type
        Drawn samples from the parameterized uniform distribution.

    """
    return _cur_framework().random_uniform(low, high, shape, dev)


def random_normal(mean=0.0, std=1.0, shape=None, dev=None):
    """Draws samples from a normal distribution.

    Parameters
    ----------
    mean : float
        The mean of the normal distribution to sample from. Default is 0.
    std : float
        The standard deviation of the normal distribution to sample from. Default is 1.
    shape :
        Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn.
        If size is None (default), a single value is returned.
    dev : ivy.Device
        device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc. (Default value = None)

    Returns
    -------
    type
        Drawn samples from the parameterized uniform distribution.

    """
    return _cur_framework().random_normal(mean, std, shape, dev)


def multinomial(population_size, num_samples, batch_size, probs=None, replace=True, dev=None):
    """Draws samples from a multinomial distribution. Specifcally, returns a tensor where each row contains num_samples
    indices sampled from the multinomial probability distribution located in the corresponding row of tensor input.

    Parameters
    ----------
    population_size : int
        The size of the population from which to draw samples.
    num_samples : int
        Number of independent samples to draw from the population.
    batch_size :
        Number of times to draw a new set of samples from the population.
    probs : array, optional
        The unnormalized probabilities for all elemtns in population,
        default is uniform *[batch_shape, num_classes]*
    replace : bool, optional
        Whether to replace samples once they've been drawn. Default is True.
    dev : ivy.Device
        device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc. (Default value = None)

    Returns
    -------
    type
        Drawn samples indices from the multinomial distribution.

    """
    return _cur_framework().multinomial(population_size, num_samples, batch_size, probs, replace, dev)


def randint(low, high, shape, dev=None):
    """Returns a tensor filled with random integers generated uniformly between low (inclusive) and high (exclusive).

    Parameters
    ----------
    low : int
        Lowest integer to be drawn from the distribution.
    high : int
        One above the highest integer to be drawn from the distribution.
    shape : sequence of ints
        a tuple defining the shape of the output tensor.
    dev : ivy.Device
        device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc. (Default value = None)

    Returns
    -------

    """
    return _cur_framework().randint(low, high, shape, dev)


def seed(seed_value=0):
    """Sets the seed for random number generation.

    Parameters
    ----------
    seed_value : int
        Seed for random number generation, must be a positive integer. (Default value = 0)

    Returns
    -------

    """
    return _cur_framework().seed(seed_value)


def shuffle(x):
    """Shuffles the given array along axis 0.

    Parameters
    ----------
    x : array
        An array object, in the specific Machine learning framework.

    Returns
    -------
    type
        An array object, shuffled along the first dimension.

    """
    return _cur_framework(x).shuffle(x)
