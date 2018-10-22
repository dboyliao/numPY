from collections import Iterable


def _gen_flatten(data):
    if not isinstance(data, Iterable):
        yield data
    else:
        for e in data:
            yield from _gen_flatten(e)


def _parse_shape(data, shape=None):
    if shape is None:
        shape = []
    if not isinstance(data, Iterable):
        return shape
    shape.append(len(data))
    elem = next(iter(data))
    return _parse_shape(elem, shape)


def parse_shape(data):
    shape = _parse_shape(data)
    return tuple(shape)


def flatten(data):
    if not data:
        return list(), ()
    return list(_gen_flatten(data))


def broadcast(arr, target_shape):
    shape = arr.shape
    target_ndim = len(target_shape)
    diff = abs(arr.ndim - target_ndim)
    if arr.ndim <= target_ndim:
        for _ in range(diff):
            shape = (1,) + shape
    else:
        for _ in range(diff):
            target_shape = (1,) + target_shape
    for this_dim, that_dim in zip(shape, target_shape):
        if this_dim == that_dim:
            continue
        elif this_dim == 1 or that_dim == 1:
            continue
        else:
            raise ValueError(f'could not broadcast input array from shape'
                             ' {arr.shape} into shape {target_shape}')
    arr_view = type(arr)([], dtype=arr.dtype)
    arr_view._data = arr._data
    return arr_view.reshape(shape)
