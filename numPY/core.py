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

    def __getitem__(self, slices):
        slices = self._validate_slices(slices)
        viewable = all([isinstance(sl, slice) for sl in slices])
        if not viewable:
            return self._make_copy(slices)
        return self._make_view(slices)

    def __setitem__(self, slices, value):
        slices = self._validate_slices(slices)
        print(slices)
        print(value)

    def __len__(self):
        return len(self._data)

    def _validate_slices(self, slices):
        if not isinstance(slices, tuple):
            slices = (slices,)
        for _ in range(self._ndim - len(slices)):
            slices += (slice(None),)
        if not len(slices) == self._ndim:
            raise IndexError('too many indices for array')
        return slices

    def _make_copy(self, indices):
        pass

    def _make_view(self, indices):
        pass

    def _iter_slices(self, slices):
        pass
