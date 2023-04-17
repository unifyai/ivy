import tensorflow as tf
from tensorflow import nn
from typing import Optional, Tuple

from functools import reduce

import ivy

from ivy.functional.ivy.experimental.linear_algebra import _check_valid_dimension_size

from ivy.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from .. import backend_version


@with_unsupported_dtypes(
    {"2.9.1 and below": ("int", "float16", "bfloat16")}, backend_version
)

def ctc_loss(
    log_probs: tf.Tensor,
    targets: tf.Tensor,
    input_lengths: tf.Tensor,
    target_lengths: tf.Tensor,
    blank: Optional[int] = 0,
    reduction: Optional[str] = "mean",
    zero_infinity: Optional[bool] = True,
    out: Optional[tf.Tensor] = None,
) -> tf.Tensor:


    #Compute the CTC loss using the Pytorch implementation
    ctc_loss = nn.ctc_loss(
        labels=tf.cast(targets, tf.int32),
        logits=log_probs,
        label_length=tf.cast(target_lengths, tf.int32),
        logit_length=tf.cast(input_lengths, tf.int32),
        )
    return tf.reduce_mean(ctc_loss)


