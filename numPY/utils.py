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


def flatten(data):
    return list(_gen_flatten(data)), _parse_shape(data)
