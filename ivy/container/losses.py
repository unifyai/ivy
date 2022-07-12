# for review
# global
from typing import Optional, Union, List, Dict

# local
import ivy
from ivy.container.base import ContainerBase


class ContainerWithLosses(ContainerBase):
    @staticmethod
    def static_cross_entropy(
        true: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        pred: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        axis: Union[int, ivy.Container] = -1,
        epsilon: Union[float, ivy.Container] = 1e-7,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        *,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.cross_entropy. This method simply
        wraps the function, and so the docstring for ivy.cross_entropy also applies
        to this method with minimal changes.

        Examples
        --------
        With :code:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([0, 0, 1]), b=ivy.array([1, 1, 0]))
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = ivy.Container.static_cross_entropy(x, y)
        >>> print(z)
        {
            a: ivy.array(1.20397282),
            b: ivy.array(1.83258148)
        }

        With a mix of :code:`ivy.Array` and :code:`ivy.Container` inputs:

        >>> x = ivy.array([0, 0, 1])
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = ivy.Container.static_cross_entropy(x, y)
        >>> print(z)
        {
            a: ivy.array(1.20397282),
            b: ivy.array(1.60943794)
        }
        """
        return ContainerBase.multi_map_in_static_method(
            "cross_entropy",
            true,
            pred,
            axis=axis,
            epsilon=epsilon,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def cross_entropy(
        self: ivy.Container,
        pred: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        axis: Union[int, ivy.Container] = -1,
        epsilon: Union[float, ivy.Container] = 1e-7,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        *,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.cross_entropy. This method simply
        wraps the function, and so the docstring for ivy.cross_entropy also applies to
        this method with minimal changes.

        Examples
        --------
        >>> x = ivy.Container(a=ivy.array([1, 0, 0]),b=ivy.array([0, 0, 1]))
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = x.cross_entropy(y)
        >>> print(z)
        {
            a:ivy.array(0.5108256),
            b:ivy.array(1.609438)
        }
        """
        return self.static_cross_entropy(
            self,
            pred,
            axis,
            epsilon,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
            out=out,
        )

    @staticmethod
    def static_binary_cross_entropy(
        true: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        pred: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        epsilon: Union[float, ivy.Container] = 1e-7,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        *,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.binary_cross_entropy. This method
        simply wraps the function, and so the docstring for ivy.binary_cross_entropy
        also applies to this method with minimal changes.

        Examples
        --------
        With :code:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([1, 0, 0]),b=ivy.array([0, 0, 1]))
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = ivy.Container.static_binary_cross_entropy(x, y)
        >>> print(z)
        {
            a: ivy.array([0.511, 0.223, 0.357]),
            b: ivy.array([1.61, 0.223, 1.61])
        }

        With a mix of :code:`ivy.Array` and :code:`ivy.Container` inputs:

        >>> x = ivy.array([1 , 1, 0])
        >>> y = ivy.Container(a=ivy.array([0.7, 0.8, 0.2]),b=ivy.array([0.2, 0.6, 0.7]))
        >>> z = ivy.Container.static_binary_cross_entropy(x, y)
        >>> print(z)
        {
            a: ivy.array([0.357, 0.223, 0.223]),
            b: ivy.array([1.61, 0.511, 1.2])
        }
        """
        return ContainerBase.multi_map_in_static_method(
            "binary_cross_entropy",
            true,
            pred,
            epsilon=epsilon,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def binary_cross_entropy(
        self: ivy.Container,
        pred: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        epsilon: Union[float, ivy.Container] = 1e-7,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        *,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.binary_cross_entropy. This
        method simply wraps the function, and so the docstring for
        ivy.binary_cross_entropy also applies to this method with minimal changes.

        Examples
        --------
        >>> x = ivy.Container(a=ivy.array([1, 0, 0]),b=ivy.array([0, 0, 1]))
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = x.binary_cross_entropy(y)
        >>> print(z)
        {
            a: ivy.array([0.511, 0.223, 0.357]),
            b: ivy.array([1.61, 0.223, 1.61])
        }
        """
        return self.static_binary_cross_entropy(
            self,
            pred,
            epsilon,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
            out=out,
        )

    @staticmethod
    def static_sparse_cross_entropy(
        true: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        pred: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        axis: Union[int, ivy.Container] = -1,
        epsilon: Union[float, ivy.Container] = 1e-7,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        *,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.sparse_cross_entropy. This method
        simply wraps the function, and so the docstring for ivy.sparse_cross_entropy
        also applies to this method with minimal changes.

        Examples
        --------
        With :code:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([1, 0, 0]),b=ivy.array([0, 0, 1]))
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = ivy.Container.static_sparse_cross_entropy(x, y)
        >>> print(z)
        {
            a: ivy.array([1.61, 0.511, 0.511]),
            b: ivy.array([0.223, 0.223, 1.61])
        }

        With a mix of :code:`ivy.Array` and :code:`ivy.Container` inputs:

        >>> x = ivy.array([1 , 1, 0])
        >>> y = ivy.Container(a=ivy.array([0.7, 0.8, 0.2]),b=ivy.array([0.2, 0.6, 0.7]))
        >>> z = ivy.Container.static_sparse_cross_entropy(x, y)
        >>> print(z)
        {
            a: ivy.array([0.223, 0.223, 0.357]),
            b: ivy.array([0.511, 0.511, 1.61])
        }
        """
        return ContainerBase.multi_map_in_static_method(
            "sparse_cross_entropy",
            true,
            pred,
            axis=axis,
            epsilon=epsilon,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def sparse_cross_entropy(
        self: ivy.Container,
        pred: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        axis: Union[int, ivy.Container] = -1,
        epsilon: Union[float, ivy.Container] = 1e-7,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        *,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.sparse_cross_entropy. This
        method simply wraps the function, and so the docstring for
        ivy.sparse_cross_entropy also applies to this method with minimal changes.

        Examples
        --------
        >>> x = ivy.Container(a=ivy.array([1, 0, 0]),b=ivy.array([0, 0, 1]))
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = x.sparse_cross_entropy(y)
        >>> print(z)
        {
            a: ivy.array([1.61, 0.511, 0.511]),
            b: ivy.array([0.223, 0.223, 1.61])
        }
        """
        return self.static_sparse_cross_entropy(
            self,
            pred,
            axis,
            epsilon,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
            out=out,
        )
