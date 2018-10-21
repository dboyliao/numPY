# -*- coding: utf8 -*-
from functools import reduce

from .utils import flatten


class NumPyArray:

    def __init__(self, data):
        flat_data, shape = flatten(data)
        assert len(flat_data) == reduce(lambda a, b: a * b, shape, 1), \
            'incorrect data shape'
        self._data = flat_data
        self._shape = tuple(shape)
        self._ndim = len(self._shape)
        self._strides = tuple(reduce(lambda a, b: a * b, self._shape[i + 1:], 1)
                              for i in range(self._ndim))

    @property
    def shape(self):
        return self._shape

    @property
    def ndim(self):
        return self._ndim

    @property
    def itemsize(self):
        elem = self._data[0]
        if isinstance(elem, (int, float)):
            return 8
        else:
            raise ValueError(f'unknown type: {type(elem)}')

    @property
    def strides(self):
        return self._strides
