# global
from typing import Any, Union, List, Dict, Iterable, Optional

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
        *,
        out: Optional[ivy.Container] = None,
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
            out=out,
        )

    @staticmethod
    def static_all_equal(
        x1: Iterable[Any],
        x2: Iterable[Any],
        equality_matrix: bool = False,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.all_equal. This method simply wraps
        the function, and so the docstring for ivy.add also applies to this method
        with minimal changes.

        Examples
        --------
        With one :code:`ivy.Container` input:
        
        >>> x1 = ivy.Container(a=ivy.array([1, 0, 1, 1]), b=ivy.array([1, -1, 0, 0]))
        >>> x2 = ivy.array([1, 0, 1, 1])
        >>> y = ivy.Container.static_all_equal(x1, x2, equality_matrix= False)
        >>> print(y)
        {
            a: ivy.array([True, True, True, True]),
            b: ivy.array([True, False, False, False])
        }
        
        With multiple :code:`ivy.Container` input:
        
        >>> x1 = ivy.Container(a=ivy.array([1, 0, 1, 1]), \
                                b=ivy.native_array([1, 0, 0, 1]))
        >>> x2 = ivy.Container(a=ivy.native_array([1, 0, 1, 1]), \
                                b=ivy.array([1, 0, -1, -1]))
        >>> y = ivy.Container.static_all_equal(x1, x2, equality_matrix= False)
        >>> print(y)
        {
            a: ivy.array([True, True, True, True]),
            b: ivy.array([True, True, False, False])
        }
        
        """
        return ContainerBase.multi_map_in_static_method(
            "all_equal",
            x1,
            x2,
            equality_matrix=equality_matrix,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def all_equal(
        self: ivy.Container,
        x2: Iterable[Any],
        equality_matrix: bool = False,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.all_equal.
        This method simply wraps the function, and so the docstring for
        ivy.all_equal also applies to this method with minimal changes.

        Examples
        --------
        With one :code:`ivy.Container` instances:

        >>> x1 = ivy.Container(a=ivy.array([1, 0, 1, 1]), b=ivy.array([1, -1, 0, 0]))
        >>> x2 = ivy.array([1, 0, 1, 1])
        >>> y = x1.all_equal(x2, equality_matrix= False)
        >>> print(y)
        {
            a: true,
            b: false
        }

        >>> x1 = ivy.Container(a=ivy.array([1, 0, 1, 1]), b=ivy.array([1, -1, 0, 0]))
        >>> x2 = ivy.array([1, 0, 1, 1])
        >>> y = ivy.Container.static_all_equal(x1, x2, equality_matrix= False)
        >>> print(y)
        {
            a: true,
            b: false
        }

        With multiple :code:`ivy.Container` instances:

        >>> x1 = ivy.Container(a=ivy.native_array([1, 0, 0]),\
                                b=ivy.array([1, 2, 3]))
        >>> x2 = ivy.Container(a=ivy.native_array([1, 0, 1]),\
                                b=ivy.array([1, 2, 3]))
        >>> y = x1.all_equal(x2, equality_matrix= False)
        >>> print(y)
        {
            a: false,
            b: true
        }

        >>> x1 = ivy.Container(a=ivy.native_array([1, 0, 0]),\
                                b=ivy.array([1, 2, 3]))
        >>> x2 = ivy.Container(a=ivy.native_array([1, 0, 1]),\
                                b=ivy.array([1, 2, 3]))
        >>> y = ivy.Container.static_all_equal(x1, x2, equality_matrix= False)
        >>> print(y)
        {
            a: false,
            b: true
        }

        """
        return self.static_all_equal(
            self,
            x2,
            equality_matrix,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
        )

    @staticmethod
    def static_gather_nd(
        params: Union[ivy.Array, ivy.NativeArray, ivy.Container],
        indices: Union[ivy.Array, ivy.NativeArray, ivy.Container],
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        *,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.gather_nd.
        This method simply wraps the function, and so the docstring
        for ivy.gather_nd also applies to this method
        with minimal changes.

        Examples
        --------
        With one :code:`ivy.Container` input:

        >>> x = ivy.Container(a=ivy.array([0., 1., 2.]), \
                              b=ivy.array([4., 5., 6.]))
        >>> y = ivy.array([1])
        >>> print(ivy.static_gather_nd(x, y))
        >>> print(z)
        {
            a: ivy.array(1.),
            b: ivy.array(5.)
        }

        With multiple :code:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([0., 1., 2.]), \
                              b=ivy.array([3., 4., 5.]))
        >>> y = ivy.Container(a=ivy.array([0]), \
                              b=ivy.array([1]))
        >>> y = ivy.Container.static_gather_nd(x, y)
        >>> print(y)
        {
                a: ivy.array(0.),
                b: ivy.array(4.)
        }
        """
        return ContainerBase.multi_map_in_static_method(
            "gather_nd",
            params,
            indices,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def gather_nd(
        self: ivy.Container,
        indices: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        *,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.gather_nd.
        This method simply wraps the function, and so the docstring
        for ivy.gather_nd also applies to this method
        with minimal changes.

        Examples
        --------
        >>> x = ivy.Container(a=ivy.array([1, 2, 3]),\
                              b=ivy.array([2, 3, 4]))
        >>> y = ivy.Container(a=ivy.array([2]),\
                              b=ivy.array([1]))
        >>> z = x.gather_nd(y)
        >>> print(z)
        {
            a: ivy.array(3),
            b: ivy.array(3)
        }
        """
        return self.static_gather_nd(
            self, indices, key_chains, to_apply, prune_unapplied, map_sequences, out=out
        )

    def to_numpy(
            self,
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.to_numpy.
        This method simply wraps the function, and so the docstring for
        ivy.to_numpy also applies to this method with minimal changes.

        Examples
        --------
        With one :code:`ivy.Container` instances:

        >>> x = ivy.Container(a=ivy.native_array([[-1, 0, 1], [-1, 0, 1], [1, 0, -1]]),\
                    b=ivy.native_array([[-1, 0, 0], [1, 0, 1], [1, 1, 1]]))
        >>> y = x.to_numpy()
        >>> print(y)
        {
            a: array([[-1, 0, 1],
                      [-1, 0, 1],
                      [1, 0, -1]], dtype=int32),
            b: array([[-1, 0, 0],
                      [1, 0, 1],
                      [1, 1, 1]], dtype=int32)
        }

        >>> x = ivy.Container(a=ivy.native_array([[-1, 0, 1], [-1, 0, 1], [1, 0, -1]]),\
                            b=ivy.native_array([[-1, 0, 0], [1, 0, 1], [1, 1, 1]]))
        >>> y = ivy.Container.static_to_numpy(x)
        >>> print(y)
        {
            a: array([[-1, 0, 1],
                      [-1, 0, 1],
                      [1, 0, -1]], dtype=int32),
            b: array([[-1, 0, 0],
                      [1, 0, 1],
                      [1, 1, 1]], dtype=int32)
        }

        """
        return self.static_to_numpy(
            self,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences
        )

    @staticmethod
    def static_to_numpy(
            x: Union[ivy.Array, ivy.NativeArray],
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.to_numpy. This method simply wraps
        the function, and so the docstring for ivy.to_numpy also applies to this method
        with minimal changes.

        Examples
        --------
        With one :code:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([1, 0, 1, 1]),\
                            b=ivy.array([1, -1, 0, 0]))
        >>> y = ivy.Container.static_to_numpy(x)
        >>> print(y)
        {
            a: array([1, 0, 1, 1], dtype=int32),
            b: array([1, -1, 0, 0], dtype=int32)
        }

        >>> x = ivy.Container(a=ivy.array([1., 0., 0., 1.]),\
                            b=ivy.native_array([1, 1, -1, 0]))
        >>> y = ivy.Container.static_to_numpy(x)
        >>> print(y)
        {
            a: array([1., 0., 0., 1.], dtype=float32),
            b: array([1, 1, -1, 0], dtype=int32)
        }

        """
        return ContainerBase.multi_map_in_static_method(
            "to_numpy",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def exists(
            self,
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.exists.
        This method simply wraps the function, and so the docstring for
        ivy.exists also applies to this method with minimal changes.

        Examples
        --------
        With one :code:`ivy.Container` instances:

        >>> x = ivy.Container(a=ivy.native_array([[-1, 0, 1], [-1, 0, 1], [1, 0, -1]]),\
                    b=ivy.native_array([[-1, 0, 0], [1, 0, 1], [1, 1, 1]]))
        >>> y = x.exists()
        >>> print(y)
        True

        >>> x = ivy.Container(a=None,\
                            b=ivy.native_array([[-1, 0, 0], [1, 0, 1], [1, 1, 1]]))
        >>> y = x.exists()
        >>> print(y)
        True

        """
        return self.static_exists(
            self,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences
        )

    @staticmethod
    def static_exists(
            x: Any,
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.exists. This method simply wraps
        the function, and so the docstring for ivy.exists also applies to this method
        with minimal changes.

        Examples
        --------
        With one :code:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([1, 0, 1, 1]),\
                            b=ivy.array([1, -1, 0, 0]))
        >>> y = ivy.Container.static_exists(x)
        >>> print(y)
        True

        >>> x = ivy.Container(a=ivy.array([1., 0., 0., 1.]),\
                            b=ivy.native_array([1, 1, -1, 0]))
        >>> y = ivy.Container.static_exists(x)
        >>> print(y)
        True

        """
        return ContainerBase.multi_map_in_static_method(
            "exists",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )
