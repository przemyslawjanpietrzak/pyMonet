.. pyMonet documentation master file, created by
   sphinx-quickstart on Sat Dec  9 19:40:35 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyMonet's documentation
===================================


.. autoclass:: pymonet.maybe.Maybe
    :members: just, nothing, map, bind, filter, get_or_else, to_either, to_lazy, to_try, to_box

.. autoclass:: pymonet.box.Box
    :members: map, bind, ap, to_maybe, to_either, to_lazy, to_try

.. autoclass:: pymonet.either.Left
    :members: map, bind, ap, is_left, is_right, to_maybe, to_either, to_lazy, to_try
.. autoclass:: pymonet.either.Right
    :members: map, bind, ap, is_left, is_right, to_maybe, to_either, to_lazy, to_try

.. autoclass:: pymonet.lazy.Lazy
    :members: __init__, __eq__, map, fold, get

.. autoclass:: pymonet.monad_try.Try
    :members: of, map, fold, filter, get_or_else, get, on_success, on_fail

.. autoclass:: pymonet.task.Task
    :members: __init__, of, reject, map, fold

.. autofunction:: pymonet.utils.identity
.. autofunction:: pymonet.utils.increase
.. autofunction:: pymonet.utils.eq
.. autofunction:: pymonet.utils.curried_map
.. autofunction:: pymonet.utils.curried_filter
.. autofunction:: pymonet.utils.compose
.. autofunction:: pymonet.utils.pipe
.. autofunction:: pymonet.utils.cond
.. autofunction:: pymonet.utils.memoize

