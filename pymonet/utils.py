from functools import reduce


def identity(value):
    return value


def increase(value):
    return value + 1


def curried_map(mapper):
    return lambda collection: [mapper(item) for item in collection]


def curried_filter(filterer):
    return lambda collection: [item for item in collection if filterer(item)]


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
