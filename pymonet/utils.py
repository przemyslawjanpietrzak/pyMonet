from functools import reduce


def identity(value):
    """
    Return first argument.

    :param value:
    :type value: Any
    :returns:
    :rtype: Any
    """
    return value


def increase(value):
    """
    Return increased by 1 argument.

    :param value:
    :type value: Int
    :returns:
    :rtype: Int
    """
    return value + 1


def eq(value, *args):
    if args:
        return value == args[0]
    return lambda other: value == other


def curried_map(mapper):
    return lambda collection: [mapper(item) for item in collection]


def curried_filter(filterer):
    return lambda collection: [item for item in collection if filterer(item)]


def find(collection, key):
    """
    Return the first element of the list which matches the keys, or None if no element matches.

    :param collection: collection to search
    :type collection: List[A]
    :param key: function to decide witch element should be found
    :type key: Function(A) -> Boolean
    :returns: element of collection or None
    :rtype: A | None
    """
    for item in collection:
        if key(item):
            return item


def compose(value, *functions):
    """
    Perform right-to-left function composition.

    :param value: argument of first applied function
    :type value: Any
    :param functions: list of functions to applied from right-to-left
    :type functions: List[Function]
    :returns: result of all functions
    :rtype: Any
    """
    return reduce(
        lambda current_value, function: function(current_value),
        functions[::-1],
        value
    )


def pipe(value, *functions):
    """
    Perform left-to-right function composition.

    :param value: argument of first applied function
    :type value: Any
    :param functions: list of functions to applied from left-to-right
    :type functions: List[Function]
    :returns: result of all functions
    :rtype: Any
    """
    return reduce(
        lambda current_value, function: function(current_value),
        functions,
        value
    )


def cond(condition_list):
    """
    Function for return function depended on first function argument
    cond get list of two-item tuples,
    first is condition_function, second is execute_function.
    Returns this execute_function witch first condition_function return truly value.

    :param condition_list: list of two-item tuples (condition_function, execute_function)
    :type condition_list: List[(Function, Function)]
    :returns: Returns this execute_function witch first condition_function return truly value
    :rtype: Function
    """
    def result(*args):
        for (condition_function, execute_function) in condition_list:
            if condition_function(*args):
                return execute_function(*args)

    return result


def memoize(fn, key=eq):
    """
    Create a new function that, when invoked,
    caches the result of calling fn for a given argument set and returns the result.
    Subsequent calls to the memoized fn with the same argument set will not result in an additional call to fn;
    instead, the cached result for that set of arguments will be returned.

    :param fn: function to invoke
    :type fn: Function(A) -> B
    :param key: function to decide if result should be taken from cache
    :type key: Function(A, A) -> Boolean
    :returns: new function invoking old one
    :rtype: Function(A) -> B
    """
    cache = []

    def memoized_fn(argument):
        cached_result = find(cache, lambda cacheItem: key(cacheItem[0], argument))
        if cached_result is not None:
            return cached_result[1]
        fn_result = fn(argument)
        cache.append((argument, fn_result))
        return fn_result

    return memoized_fn
