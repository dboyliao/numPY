# -*- coding: utf8 -*-
from collections import Iterable
from functools import reduce
from itertools import product

from .utils import flatten


class NumPyArray:

    def __init__(self, data):
        flat_data, shape = flatten(data)
        self._data = flat_data
        self._reshape(tuple(shape))

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

    def reshape(self, new_shape):
        ori_n = reduce(lambda a, b: a * b, self._shape, 1)
        new_n = reduce(lambda a, b: a * b, new_shape, 1)
        if ori_n != new_n:
            raise ValueError(f'incompatible shape: {new_shape}')
        return self._reshape(new_shape)

    def _reshape(self, new_shape):
        self._shape = new_shape
        self._ndim = len(self._shape)
        self._strides = tuple(reduce(lambda a, b: a * b, self._shape[i + 1:], 1)
                              for i in range(self._ndim))
        return self

    def _validate_slices(self, slices):
        if not isinstance(slices, tuple):
            slices = (slices,)
        for _ in range(self._ndim - len(slices)):
            slices += (slice(None),)
        valid_slices = [sl for sl in slices if sl is not None]
        if not len(valid_slices) == self._ndim:
            raise IndexError('too many indices for array')
        return slices

    def _make_copy(self, slices):
        # copy data
        new_data = []
        for idxs in self._iter_slices(slices):
            offset = sum([idx * stride
                          for (idx, stride) in zip(idxs, self._strides)])
            new_data.append(self._data[offset])
        # reshape
        new_shape = self._infer_shape(slices)
        new_arr = NumPyArray(new_data)
        new_arr._reshape(new_shape)
        return new_arr

    def _make_view(self, slices):
        new_arr = NumPyArray([])
        new_arr._data = self._data
        new_shape = self._infer_shape(slices)
        return new_arr._reshape(new_shape)

    def _infer_shape(self, slices):
        new_shape = ()
        idx_dim = 0
        for sl in slices:
            if sl is None:
                new_dim = (1,)
            elif isinstance(sl, slice):
                dim = self._shape[idx_dim]
                start, end, step = sl.indices(dim)
                new_dim = (len(range(start, end, step)),)
                idx_dim += 1
            elif isinstance(sl, Iterable):
                new_dim = (len(list(sl)),)
                idx_dim += 1
            elif isinstance(sl, int):
                new_dim = (1,)
                idx_dim += 1
            else:
                raise ValueError(f'unsupport indices type: {type(sl)}')
            new_shape += new_dim
        return new_shape

    def _iter_slices(self, slices):
        iters = []
        new_shape = self._infer_shape(slices)
        for sl, dim in zip(slices, new_shape):
            if isinstance(sl, slice):
                start, end, step = sl.indices(dim)
                iters.append(range(start, end, step))
            elif isinstance(sl, Iterable):
                iters.append(sl)
            elif sl is None:
                iters.append([0])
            else:
                raise ValueError(f'invalid indices type: {type(sl)}')
        yield from product(*iters)
