Try
*********

.. code-block:: python
    :caption: example_try.py
    :name: example_try-py

    from pymonet.monad_try import Try

    def divide(dividend, divisor):
        return dividend / divisor

    def success_callback(value):
        print('success: {}'.format(value))

    def fail_callback(error):
        print('error: {}'.format(value))

    (Try.of(divide, 42, 2)
        .on_success(success_callback)
        .on_fail(fail_callback))
    # success: 21

    (Try.of(divide, 42, 0)
        .on_success(success_callback)
        .on_fail(fail_callback))
    #error: division by zero

    # map method will be only applied mapper when exception was not thrown

    (Try.of(divide, 42, 2)
        .map(lambda value: value + 1)
        .on_success(success_callback)
        .on_fail(fail_callback))
    # success: 22

    (Try.of(divide, 42, 0)
        .on_success(success_callback)
        .map(lambda value: value + 1)
        .on_fail(fail_callback))
    #error: division by zero
    
    # get_or_else method returns value when exception was not thrown
    
    Try.of(divide, 42, 2).get_or_else('Holy Grail') # 21
    Try.of(divide, 42, 0).get_or_else('Holy Grail') # 'Holy Grail'
    
    # get method should return value with or without exception thrown
    
    Try.of(divide, 42, 2).get()  # 21
    Try.of(divide, 42, 0).get()  # ZeroDivisionError<'division by zero'>


.. autoclass:: pymonet.monad_try.Try
    :members: of, map, bind, filter, get_or_else, get, on_success, on_fail
