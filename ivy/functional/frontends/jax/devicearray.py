# local
import ivy
import ivy.functional.frontends.jax as jax_frontend


class DeviceArray:
    def __init__(self, data):
        if ivy.is_native_array(data):
            data = ivy.Array(data)
        self.data = data

    # Instance Methods #
    # ---------------- #

    def reshape(self, new_sizes, dimensions=None):
        return jax_frontend.reshape(self.data, new_sizes, dimensions)

    def add(self, other):
        return jax_frontend.add(self.data, other)

    # Special Methods #
    # --------------- #

    def __pos__(self):
        return ivy.positive(self.data)

    def __neg__(self):
        return jax_frontend.neg(self.data)

    def __eq__(self, other):
        return jax_frontend.eq(self.data, other)

    def __ne__(self, other):
        return jax_frontend.ne(self.data, other)

    def __lt__(self, other):
        return jax_frontend.lt(self.data, other)

    def __le__(self, other):
        return jax_frontend.le(self.data, other)

    def __gt__(self, other):
        return jax_frontend.gt(self.data, other)

    def __ge__(self, other):
        return jax_frontend.ge(self.data, other)

    def __abs__(self):
        return jax_frontend.abs(self.data)
