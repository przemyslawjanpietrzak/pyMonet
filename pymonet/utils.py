from functools import reduce


def identity(value):
    return value


def increase(value):
    return value + 1


def compose(value, *functions):
    return reduce(
        lambda current_value, function: function(current_value),
        functions[::-1],
        value
    )

def pipe(value, *functions):
    return reduce(
        lambda current_value, function: function(current_value),
        functions,
        value
    )

def curried_map(mapper):
    return lambda lst: list(map(mapper, lst))


def curried_filter(filterer):
    return lambda lst: list(filter(filterer, lst))
