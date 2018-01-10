Box
*********



.. code-block:: python
   :caption: example_box.py
   :name: example_box-py

   from pymonet.box import Box
   box = Box(42)  # Box<42>
   (box
       .map(lambda value: value + 1)  # Box<43>
       .map(lambda value: str(value))  # Box<"43">
       .map(lambda value: value[::-1])  # Box<"34">
       .bind(lambda value: "output = " + value))  # "output = 34"

.. autoclass:: pymonet.box.Box
    :members: map, bind, ap, to_maybe, to_either, to_lazy, to_try, to_validation