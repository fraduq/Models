# -*- coding: utf-8 -*-
# MegEngine is Licensed under the Apache License, Version 2.0 (the "License")
#
# Copyright (c) 2014-2020 Megvii Inc. All rights reserved.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT ARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import megengine as mge
import megengine.functional as F
import numpy as np

from megengine import _internal as mgb
from megengine.core import Tensor, wrap_io_tensor


def get_padded_array_np(
    array: np.ndarray, multiple_number: int = 32, pad_value: float = 0
) -> np.ndarray:
    """ pad the nd-array to multiple stride of th e

    Args:
        array (np.ndarray):
            the array with the shape of [batch, channel, height, width]
        multiple_number (int):
            make the height and width can be divided by multiple_number
        pad_value (int): the value to be padded

    Returns:
        padded_array (np.ndarray)
    """
    batch, chl, t_height, t_width = array.shape
    padded_height = (
        (t_height + multiple_number - 1) // multiple_number * multiple_number
    )
    padded_width = (t_width + multiple_number - 1) // multiple_number * multiple_number

    padded_array = (
        np.ones([batch, chl, padded_height, padded_width], dtype=np.float32) * pad_value
    )

    ndim = array.ndim
    if ndim == 4:
        padded_array[:, :, :t_height, :t_width] = array
    elif ndim == 3:
        padded_array[:, :t_height, :t_width] = array
    else:
        raise Exception("Not supported tensor dim: %d" % ndim)
    return padded_array


def get_padded_tensor(
    array: Tensor, multiple_number: int = 32, pad_value: float = 0
) -> Tensor:
    """ pad the nd-array to multiple stride of th e

    Args:
        array (Tensor):
            the tensor with the shape of [batch, channel, height, width]
        multiple_number (int):
            make the height and width can be divided by multiple_number
        pad_value (int): the value to be padded

    Returns:
        padded_array (Tensor)
    """
    batch, chl, t_height, t_width = array.shape
    padded_height = (
        (t_height + multiple_number - 1) // multiple_number * multiple_number
    )
    padded_width = (t_width + multiple_number - 1) // multiple_number * multiple_number

    padded_array = (
        mge.ones(
            F.concat([batch, chl, padded_height, padded_width], axis=0),
            dtype=np.float32,
        )
        * pad_value
    )

    ndim = array.ndim
    if ndim == 4:
        padded_array = padded_array.set_subtensor(array)[:, :, :t_height, :t_width]
    elif ndim == 3:
        padded_array = padded_array.set_subtensor(array)[:, :t_height, :t_width]
    else:
        raise Exception("Not supported tensor dim: %d" % ndim)
    return padded_array


@wrap_io_tensor
def indexing_set_one_hot(inp, axis, idx, value) -> Tensor:
    return mgb.opr.indexing_set_one_hot(inp, axis, idx, value)
