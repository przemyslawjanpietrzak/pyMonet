ImmutableList
*********

.. code-block:: python
    :caption: example_immutable_list.py
    :name: example_immutable_list-py

    from pymonet.immutable_list import ImmutableList
    from pymonet.utils import increase

    lst = ImmutableList.of(1, 2, 3)

    lst.map(increase) # ImmutableList.of(2, 3, 4)
    lst.filter(lambda item: item % 2 == 0) # ImmutableList.of(2)
    lst.find(lambda item: item % 2 == 0) # 2
    lst.map(increase) # ImmutableList.of(2, 3, 4)


.. autoclass:: pymonet.immutable_list.ImmutableList
    :members: __add__, of, empty, to_list, length, append, map, filter, unshift, find, reduce
