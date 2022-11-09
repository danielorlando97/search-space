from itertools import zip_longest
from typing import Iterable, Iterator


def mapper(a, b, f):
    for item in a:
        yield f(item, b)


def rmapper(a, b, f):
    try:
        for item in b:
            yield f(a, item)
    except TypeError:
        return f(a, b)


def map_reduce(a, b, f):
    try:
        iter_ = zip(a, b)

    except TypeError:
        if isinstance(a, Iterator):
            return mapper(a, b, f)
        else:
            return rmapper(a, b, f)

    for item_a, item_b in iter_:
        yield f(item_a, item_b)


def map_reduce_longest(a, b, f, zero=0):
    try:
        iter_ = zip_longest(a, b, fillvalue=zero)

    except TypeError:
        if isinstance(a, Iterator):
            return mapper(a, b, f)
        else:
            return rmapper(a, b, f)

    for item_a, item_b in iter_:
        yield f(item_a, item_b)


def compare(a, b, f):
    while True:
        try:
            item = next(a)
        except TypeError:
            item = a

        try:
            list_ = list(b)
        except TypeError:
            yield f(item, b)

        result = True
        for item_b in list_:
            result &= f(item, item_b)

        yield result


def filter(a, b, f):
    while True:
        try:
            item = next(a)
        except TypeError:
            item = a

        try:
            list_ = list(b)
        except TypeError:
            result = f(item, b)
            if not result:
                continue
            yield item

        result = True
        for item_b in list_:
            result &= f(item, item_b)

        if not result:
            continue

        yield item


def is_iterable(item):
    return isinstance(item, Iterable) and not isinstance(item, str)
