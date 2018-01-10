Either
*********

.. code-block:: python
    :caption: example_either.py
    :name: example_either-py

    from pymonet.either import Left, Right
    from pymonet.utils import identity

    def divide(divided, divider):
        if divider == 0:
            return Left('can not divide by 0')
        return Right(divided, divider)

    def handle_error(value):
        print ('error {}'.format(value))

    def handle_success(value):
        print ('success {}'.format(value))

    (divide(42, 0)
        .map(lambda value: value + 1)
        .bind(lambda value: Right(value + 1))
        .case(error=handle_error, success=handle_success))
    # error 42

    (divide(42, 1)
        .map(identity, lambda value: value + 1)
        .bind(lambda value: Right(value + 1))
        .case(error=handle_error, success=handle_success))
    # success  44


.. autoclass:: pymonet.either.Left
    :members: map, bind, ap, is_left, is_right, to_maybe, to_either, to_lazy, to_try, to_validation
.. autoclass:: pymonet.either.Right
    :members: map, bind, ap, is_left, is_right, to_maybe, to_either, to_lazy, to_try, to_validation
