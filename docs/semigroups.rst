Semigroups
*********

.. code-block:: python
    :caption: example_semigroup.py
    :name: example_semigroup-py

    from pymonet.semigroups import All, First, Map, Sum

    All(True).concat(All(False))  # All<False>
    All(True).concat(All(True))  # All<True>

    All(True) == All(True)  # True
    All(True) == All(False)  # False

    ingredient1 = Map({'score': Sum(1), 'won': All(True), 'captain': First('captain america')})
    ingredient2 = Map({'score': Sum(2), 'won': All(True), 'captain': First('iron man')})
    ingredient1.concat(ingredient2)  # Map<{'score': Sum(3), 'won': All(True), 'captain': First('captain america')}>

.. autoclass:: pymonet.semigroups.All
.. autoclass:: pymonet.semigroups.One
.. autoclass:: pymonet.semigroups.First
.. autoclass:: pymonet.semigroups.Map

