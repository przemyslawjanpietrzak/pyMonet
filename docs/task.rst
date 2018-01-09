Task
*********

.. code-block:: python
    :caption: example_box.py
    :name: example_box-py

    from pymonet.task import Task

    def resolvable_fn(reject, resolve):
        print('resolve side effect')
        resolve(42)

    def rejectable_fn(reject, resolve):
        print('reject side effect')
        reject(0)

    resolvable_task = Task.of(resolvable_fn)
    rejectable_task = Task.of(rejectable_fn)

    # map method will be applied only on resolvable tasks during calling fold method

    resolvable_task.map(lambda value: value + 1)  # Task<() -> 43>
    rejectable_task.map(lambda value: value + 1)  # Task<() -> 0>

    # fold method will be applied only on resolvable tasks. Fold also will call stored function

    def mapper(value):
        print('mapper side effect ' + value)
        return value + 1

    resolvable_task.fold(mapper)
    # resolve side effect
    # mapper side effect 42

    rejectable_task.fold(mapper)
    # reject side effect

.. autoclass:: pymonet.task.Task
    :members: __init__, of, reject, map, bind, to_validation
