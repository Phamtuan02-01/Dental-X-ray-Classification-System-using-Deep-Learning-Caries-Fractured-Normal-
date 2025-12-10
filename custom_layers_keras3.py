"""
Custom Layers và CBAM Module cho Keras 3
"""
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'

import keras
from keras.layers import (GlobalAveragePooling2D, GlobalMaxPooling2D,
                          Reshape, Dense, Add, Multiply, Concatenate, Conv2D)
from keras import ops


class KerasMean(keras.layers.Layer):
    """Custom layer cho ops.mean"""
    def __init__(self, axis=None, keepdims=False, **kwargs):
        self._axis = axis
        self._keepdims = keepdims
        kwargs.pop('initial', None)
        super().__init__(**kwargs)

    def call(self, inputs):
        return ops.mean(inputs, axis=self._axis, keepdims=self._keepdims)

    def get_config(self):
        config = super().get_config()
        config.update({
            'axis': self._axis,
            'keepdims': self._keepdims,
        })
        return config


class KerasMax(keras.layers.Layer):
    """Custom layer cho ops.max"""
    def __init__(self, axis=None, keepdims=False, **kwargs):
        self._axis = axis
        self._keepdims = keepdims
        kwargs.pop('initial', None)
        super().__init__(**kwargs)

    def call(self, inputs):
        return ops.max(inputs, axis=self._axis, keepdims=self._keepdims)

    def get_config(self):
        config = super().get_config()
        config.update({
            'axis': self._axis,
            'keepdims': self._keepdims,
        })
        return config


def channel_attention_module(x, ratio=8):
    """CBAM Channel Attention Module"""
    avg_pool = GlobalAveragePooling2D()(x)
    max_pool = GlobalMaxPooling2D()(x)
    avg_pool = Reshape((1, 1, avg_pool.shape[1]))(avg_pool)
    max_pool = Reshape((1, 1, max_pool.shape[1]))(max_pool)
    shared_dense_one = Dense(x.shape[-1] // ratio, activation='relu')
    shared_dense_two = Dense(x.shape[-1])
    avg_out = shared_dense_two(shared_dense_one(avg_pool))
    max_out = shared_dense_two(shared_dense_one(max_pool))
    cbam_feature = Add()([avg_out, max_out])
    return Multiply()([x, cbam_feature])


def spatial_attention_module(x):
    """CBAM Spatial Attention Module"""
    avg_pool = ops.mean(x, axis=-1, keepdims=True)
    max_pool = ops.max(x, axis=-1, keepdims=True)
    concat = Concatenate()([avg_pool, max_pool])
    cbam_feature = Conv2D(1, kernel_size=7, padding='same', activation='sigmoid')(concat)
    return Multiply()([x, cbam_feature])


def cbam_block(x):
    """CBAM Block kết hợp Channel và Spatial Attention"""
    x = channel_attention_module(x)
    x = spatial_attention_module(x)
    return x
