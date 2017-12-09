.. pyMonet documentation master file, created by
   sphinx-quickstart on Sat Dec  9 19:40:35 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyMonet's documentation!
===================================



.. autoclass:: pymonet.maybe.Maybe
    :members: just, nothing, map, bind, filter, get_or_else

.. autoclass:: pymonet.box.Box
    :members: bind, map

.. autofunction:: pymonet.utils.pipe
.. autofunction:: pymonet.utils.cond

.. autoclass:: pymonet.either.Left
    :members: bind, map

.. function:: format_exception(etype, value, tb[, limit=None])

    Format the exception with a traceback.

    :param etype: exception type
    :param value: exception value
    :param tb: traceback object
    :param limit: maximum number of stack frames to show
    :type limit: integer or None
    :param condition_list: list of two-item tuples (condition_function, execute_function)
    :type condition_list: List<(Function, Function)>
    :returns: Returns this execute_function witch first condition_function return truly value
    :rtype: Function
    