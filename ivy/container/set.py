# global
from typing import Dict, List, Optional, Union

# local
import ivy
from ivy.container.base import ContainerBase
import ivy
from typing import Optional, List, Union, Dict

# ToDo: implement all methods here as public instance methods


# noinspection PyMissingConstructor
class ContainerWithSet(ContainerBase):

    @staticmethod
    def static_unique_all(
            x: Union[ivy.Array, ivy.NativeArray, ivy.Container],
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        return ContainerBase.multi_map_in_static_method(
            "unique_all",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences
        )

    def unique_all(
            self: ivy.Container,
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        return self.static_unique_all(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences
        )

    @staticmethod
    def static_unique_counts(
        x: ivy.Container,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.unique_counts. This method simply 
        wraps the function, and so the docstring for ivy.unique_counts also applies 
        to this method with minimal changes.

        Examples
        --------
        With :code:`ivy.Container` static instance method:

        >>> x = ivy.Container(a=ivy.array([0., 1., 3. , 2. , 1. , 0.]), \
                              b=ivy.array([1,2,1,3,4,1,3]))
        >>> y = ivy.static_unique_counts(x)
        >>> print(y)
        {
            a: (list[2],<classivy.array.Array>shape=[4]),
            b: (list[2],<classivy.array.Array>shape=[4])
        }
        """
        return ContainerBase.multi_map_in_static_method(
            "unique_counts",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences
        )

    def unique_counts(
            self: ivy.Container,
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.unique_counts. This method
        simply wraps the function, and so the docstring for ivy.unique_counts
        also applies to this method with minimal changes.
        Examples
        --------
        With :code:`ivy.Container` instance method:
        >>> x = ivy.Container(a=ivy.array([0., 1., 3. , 2. , 1. , 0.]), \
                              b=ivy.array([1,2,1,3,4,1,3]))
        >>> y = x.unique_counts()
        >>> print(y)
        {
            a: (list[2],<classivy.array.Array>shape=[4]),
            b: (list[2],<classivy.array.Array>shape=[4])
        }
        """
        return self.static_unique_counts(
            self, key_chains, to_apply, prune_unapplied, map_sequences
        )

    @staticmethod
    def static_unique_values(
            x: Union[ivy.Array, ivy.NativeArray, ivy.Container],
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False,
            *,
            out: Optional[ivy.Container] = None
    ) -> ivy.Container:
        return ContainerBase.multi_map_in_static_method(
            "unique_values",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out
        )

    def unique_values(
            self: ivy.Container,
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False,
            *,
            out: Optional[ivy.Container] = None
    ) -> ivy.Container:
        return self.static_unique_values(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out
        )

    @staticmethod
    def static_unique_inverse(
            x: Union[ivy.Array, ivy.NativeArray, ivy.Container],
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        return ContainerBase.multi_map_in_static_method(
            "unique_inverse",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences
        )

    def unique_inverse(
            self: ivy.Container,
            key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
            to_apply: bool = True,
            prune_unapplied: bool = False,
            map_sequences: bool = False
    ) -> ivy.Container:
        return self.static_unique_inverse(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences
        )
