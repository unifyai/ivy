from typing import Optional, Union, List, Dict

# local
import ivy
from ivy.container.base import ContainerBase

# ToDo: implement all methods here as public instance methods


# noinspection PyMissingConstructor
class ContainerWithGradients(ContainerBase):
    @staticmethod
    def static_optimizer_update(
        ws,
        effective_grads,
        lr,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ) -> ivy.Container:

        return ContainerBase.multi_map_in_static_method(
            "optimizer_update",
            ws,
            effective_grads,
            lr,
            inplace=inplace,
            stop_gradients=stop_gradients,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def optimizer_update(
        self: ivy.Container,
        ws,
        effective_grads,
        lr,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ) -> ivy.Container:
        return self.static_optimizer_update(
            self,
            ws,
            effective_grads,
            lr,
            inplace,
            stop_gradients,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
        )

    @staticmethod
    def static_gradient_descent_update(
        ws,
        dcdws,
        lr,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ) -> ivy.Container:

        return ContainerBase.multi_map_in_static_method(
            "gradient_descent_update",
            ws,
            dcdws,
            lr,
            inplace=inplace,
            stop_gradients=stop_gradients,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def gradient_descent_update(
        self,
        ws,
        dcdws,
        lr,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ):
        return self.static_gradient_descent_update(
            self,
            ws,
            dcdws,
            lr,
            inplace,
            stop_gradients,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
        )

    @staticmethod
    def static_lars_update(
        ws,
        dcdws,
        lr,
        decay_lambda=0,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ) -> ivy.Container:
        return ContainerBase.multi_map_in_static_method(
            "lars_update",
            ws,
            dcdws,
            lr,
            decay_lambda=decay_lambda,
            inplace=inplace,
            stop_gradients=stop_gradients,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def lars_update(
        self,
        ws,
        dcdws,
        lr,
        decay_lambda=0,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ):
        return self.static_lars_update(
            self,
            ws,
            dcdws,
            lr,
            decay_lambda,
            inplace,
            stop_gradients,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
        )

    @staticmethod
    def static_adam_update(
        ws,
        dcdws,
        lr,
        mw_tm1,
        vw_tm1,
        step,
        beta1=0.9,
        beta2=0.999,
        epsilon=1e-7,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ) -> ivy.Container:
        return ContainerBase.multi_map_in_static_method(
            "adam_update",
            ws,
            dcdws,
            lr,
            mw_tm1=mw_tm1,
            vw_tm1=vw_tm1,
            step=step,
            beta1=beta1,
            beta2=beta2,
            epsilon=epsilon,
            inplace=inplace,
            stop_gradients=stop_gradients,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def adam_update(
        self,
        ws,
        dcdws,
        lr,
        mw_tm1,
        vw_tm1,
        step,
        beta1=0.9,
        beta2=0.999,
        epsilon=1e-7,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ):
        return self.static_adam_update(
            self,
            ws,
            dcdws,
            lr,
            mw_tm1,
            vw_tm1,
            step,
            beta1,
            beta2,
            epsilon,
            inplace,
            stop_gradients,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
        )

    @staticmethod
    def static_lamb_update(
        ws,
        dcdws,
        lr,
        mw_tm1,
        vw_tm1,
        step,
        beta1=0.9,
        beta2=0.999,
        epsilon=1e-7,
        max_trust_ratio=10,
        decay_lambda=0,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ) -> ivy.Container:
        return ContainerBase.multi_map_in_static_method(
            "lamb_update",
            ws,
            dcdws,
            lr,
            mw_tm1=mw_tm1,
            vw_tm1=vw_tm1,
            step=step,
            beta1=beta1,
            beta2=beta2,
            epsilon=epsilon,
            max_trust_ratio=max_trust_ratio,
            decay_lambda=0,
            inplace=inplace,
            stop_gradients=stop_gradients,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def lamb_update(
        self,
        ws,
        dcdws,
        lr,
        mw_tm1,
        vw_tm1,
        step,
        beta1=0.9,
        beta2=0.999,
        epsilon=1e-7,
        max_trust_ratio=10,
        decay_lambda=0,
        inplace=None,
        stop_gradients=True,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
    ):
        return self.static_lamb_update(
            self,
            ws,
            dcdws,
            lr,
            mw_tm1,
            vw_tm1,
            step,
            beta1,
            beta2,
            epsilon,
            max_trust_ratio,
            decay_lambda,
            inplace,
            stop_gradients,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
        )
