from functools import reduce


def identity(value):
    return value


def increase(value):
    return value + 1


def curried_map(mapper):
    return lambda lst: list(map(mapper, lst))


def curried_filter(filterer):
    return lambda lst: list(filter(filterer, lst))


def compose(value, *functions):
    """
    Performs right-to-left function composition.
    :param value - argument of first applied function
    :type Any
    :param functions - list of functions to applied from right-to-left
    :return result of all functions
    :typa Any
    """
    return reduce(
        lambda current_value, function: function(current_value),
        functions[::-1],
        value
    )


def pipe(value, *functions):
    """
    Performs ledt-to-right function composition.
    :param value - argument of first applied function
    :type Any
    :param functions - list of functions to applied from ledt-to-right
    :return result of all functions
    :typa Any
    """
    return reduce(
        lambda current_value, function: function(current_value),
        functions,
        value
    )
