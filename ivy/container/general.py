# local
from ivy.container.base import ContainerBase
import ivy

# ToDo: implement all methods here as public instance methods


# noinspection PyMissingConstructor
class ContainerWithGeneral(ContainerBase):
    def clip_vector_norm(
        self,
        max_norm,
        p,
        global_norm=False,
        key_chains=None,
        to_apply=True,
        prune_unapplied=False,
        map_sequences=False,
        out=None,
    ):
        max_norm_is_container = isinstance(max_norm, ivy.Container)
        p_is_container = isinstance(p, ivy.Container)
        if global_norm:
            if max_norm_is_container or p_is_container:
                raise Exception(
                    """global_norm can only be computed for 
                    scalar max_norm and p_val arguments,"""
                    "but found {} and {} of type {} and {} respectively".format(
                        max_norm, p, type(max_norm), type(p)
                    )
                )
            vector_norm = self.vector_norm(p, global_norm=True)
            ratio = max_norm / vector_norm
            if ratio < 1:
                return self.handle_inplace(self * ratio, out)
            return self.handle_inplace(self.copy(), out)
        return self.handle_inplace(
            self.map(
                lambda x, kc: self._ivy.clip_vector_norm(
                    x,
                    max_norm[kc] if max_norm_is_container else max_norm,
                    p[kc] if p_is_container else p,
                )
                if self._ivy.is_native_array(x) or isinstance(x, ivy.Array)
                else x,
                key_chains,
                to_apply,
                prune_unapplied,
                map_sequences,
            ),
            out,
        )


    def all_equal(
        x1: Union[ivy.Array, ivy.NativeArray, ivy.Container],
        x2: Union[ivy.Array, ivy.NativeArray, ivy.Container],
        equality_matrix: bool = False
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.all_equal. This method is
        determines whether the inputs are all equal.

        Examples
        --------

        With one :code:`ivy.Container` input:

        >>> x1 = ivy.Container(a=ivy.array([1, 0, 1, 1]),\
                                b=ivy.array([1, -1, 0, 0]))
        >>> x2 = ivy.array([1, 0, 1, 1])
        >>> y = ivy.all_equal(x1, x2, equality_matrix= False)
        >>> print(y)
        {
            a: true,
            b: false
        }

        >>> x1 = ivy.Container(a=ivy.array([1, 0, 1, 1]),\
                                b=ivy.array([1, -1, 0, 0]))
        >>> x2 = ivy.array([1, -1, 0, 0])
        >>> y = ivy.all_equal(x1, x2, equality_matrix= True)
        >>> print(y)
        {
            a: ivy.array([[True, False],\
                         [False, True]])
            b: ivy.array([[True, True],\
                         [True, True]]),
        }

        >>> x1 = ivy.Container(a=ivy.native_array([1, 0, 1, 1]),\
                                b=ivy.native_array([1, -1, 0, 0]))
        >>> x2 = ivy.native_array([1, 0, 1, 1])
        >>> y = ivy.all_equal(x1, x2, equality_matrix= False)
        >>> print(y)
        {
            a: true,
            b: false
        }

        >>> x1 = ivy.Container(a=ivy.native_array([1, 0, 1, 1]),\
                                b=ivy.native_array([1, -1, 0, 0]))
        >>> x2 = ivy.native_array([1, -1, 0, 0])
        >>> y = ivy.all_equal(x1, x2, equality_matrix= True)
        >>> print(y)
        {
            a: ivy.array([[True, False],\
                         [False, True]])
            b: ivy.array([[True, True],\
                         [True, True]]),
        }

        With multiple :code:`ivy.Container` inputs:

        >>> x1 = ivy.Container(a=ivy.native_array([1, 0, 0]),\
                            b=ivy.array([1, 2, 3]))
        >>> x2 = ivy.Container(a=ivy.native_array([1, 0, 1]),\
                                b=ivy.array([1, 2, 3]))
        >>> y = ivy.all_equal(x1, x2, equality_matrix= False)
        >>> print(y)
        {
            a: false,
            b: true
        }

        >>> x1 = ivy.Container(a=ivy.array([1, 0, 0]),\
                                b=ivy.native_array([1, 0, 1]))
        >>> x2 = ivy.Container(a=ivy.native_array([1, 0, 0]),\
                                b=ivy.native_array([1, 2, 3]))
        >>> y = ivy.all_equal(x1, x2, equality_matrix= True)
        >>> print(y)
        {
            a: ivy.array([[True, True],\
                         [True, True]]),
            b: ivy.array([[True, False],\
                         [False, True]])
        }

        """
        equality_fn = ivy.array_equal if ivy.is_native_array(xs[0]) else lambda a, b: a == b
        if equality_matrix:
            num_arrays = len(xs)
            mat = [[None for _ in range(num_arrays)] for _ in range(num_arrays)]
            for i, xa in enumerate(xs):
                for j_, xb in enumerate(xs[i:]):
                    j = j_ + i
                    res = equality_fn(xa, xb)
                    if ivy.is_native_array(res):
                        # noinspection PyTypeChecker
                        res = ivy.to_scalar(res)
                    # noinspection PyTypeChecker
                    mat[i][j] = res
                    # noinspection PyTypeChecker
                    mat[j][i] = res
            return ivy.array(mat)
        x0 = xs[0]
        for x in xs[1:]:
            if not equality_fn(x0, x):
                return False
        return True
