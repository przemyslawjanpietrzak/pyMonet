Maybe
*********

.. code-block:: python
    :caption: example_maybe.py
    :name: example_maybe-py

    from pymonet.Maybe import Maybe


    def get_index(item):
        if item in [1,2,3]:
            return Maybe.just(42)
        return Maybe.nothing()

    get_index(42).get_or_else(0)  # 0
    get_index(1).get_or_else(0)  # 3

    get_index(42)\
        .map(lambda value: value + 1)\
        .bind(lambda value: Maybe.just(value + 1))\
        .get_or_else(0)
        # 0

    get_index(1)\
        .map(lambda value: value + 1)\
        .bind(lambda value: Maybe.just(value + 1))\
        .get_or_else(0)

    get_index(42)\
        .filter(lambda value: value % 2 == 0)\
        .get_or_else(0)
    # 0

    get_index(3)\
        .filter(lambda value: value % 2 == 0)\
        .get_or_else(0)
    # 0

    get_index(2)\
        .filter(lambda value: value % 2 == 0)\
        .get_or_else(0)
    # 2

.. autoclass:: pymonet.maybe.Maybe
    :members: just, nothing, map, bind, filter, get_or_else, to_either, to_lazy, to_try, to_box, to_validation