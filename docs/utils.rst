Utils
*********

.. autofunction:: pymonet.utils.identity
.. autofunction:: pymonet.utils.increase
.. autofunction:: pymonet.utils.eq
.. autofunction:: pymonet.utils.curried_map
.. autofunction:: pymonet.utils.curried_filter
.. autofunction:: pymonet.utils.compose
.. code-block:: python
    :caption: example_compose.py
    :name: example_compose-py

    from pymonet.utils import \
        increase,\
        compose,\
        curried_map as map,\
        curried_filter as filter

    compose(
        list(range(10)),
        map(increase),
        filter(is_odd)
    )
    #[1, 3, 5, 7, 9]

.. autofunction:: pymonet.utils.pipe
.. code-block:: python
    :caption: example_pipe.py
    :name: example_pipe-py

    from pymonet.utils import increase, pipe

    pipe(42, increase, lambda value: value * 2)
    #86

.. autofunction:: pymonet.utils.curry
.. code-block:: python
    :caption: example_curry.py
    :name: example_curry-py

    from pymonet.utils import curry

    @curry
    def fn(arg1, arg2, arg3):
        return arg1 + arg2 + arg3

    fn(1)(2)(3) # 6
    fn(1, 2)(3) # 6
    fn(1)(2, 3) # 6
    fn(1, 2, 3) # 6


.. autofunction:: pymonet.utils.cond
.. code-block:: python
    :caption: example_cond.py
    :name: example_cond-py

    from pymonet.utils import cond

    fn = cond([
        (lambda arg: arg == 0, lambda: 'first'),
        (lambda arg: arg == 1, lambda: 'second'),
        (lambda arg: arg == 2, lambda: 'third').
    ])
    fn(1) #  second
    # lambda arg: arg == 2 will not be call

.. autofunction:: pymonet.utils.memoize
.. code-block:: python
    :caption: example_memoize.py
    :name: example_memoize-py

    from pymonet.utils import memoize, eq

    def fn(arg):
        print('fn flag')
        return arg + 1

    memoized_fn = memoize(fn)
    memoized_fn(42) # 43
    # fn flag

    memoized_fn(42) # 43
    # print to called

    memoized_fn(43) # 44
    # fn flag


