Lazy
*********


.. code-block:: python
    :caption: example_try.py
    :name: example_try-py

    from pymonet.lazy import Lazy

    def fn():
        print('fn call')
        return 42

    def mapper(value):
        print('mapper side effect of ' + value)
        return value + 1

    def side_effect(value):
        print('side effect of ' + value)

    # Lazy instances memoize output of constructor function
    lazy = Lazy(fn)
    mapped_lazy = lazy.map(mapper)
    mapped_lazy.fold(side_effect)  
    # fn call
    # mapper side effect of 42
    # side effect of 42
    lazy = Lazy(fn)
    value1 = lazy.get()
    # fn call
    value2 = lazy.get()
    print(value1, value2)
    # 42, 42

.. autoclass:: pymonet.lazy.Lazy
    :members: __init__, __eq__, of, map, bind, get, to_validation
