Validation
*********

.. code-block:: python
   :caption: example_validation.py
   :name: example_validation-py

    from pymonet.validation import Validation


    def test_validation_is_fail():
        assert Validation.fail(['fail']).is_fail()


    def validate_length(value):
        if len(value) < 5:
            return Validation.fail(['value not long enough'])
        return Validation.success()


    def validate_uppercase(value):
        if value[0].upper() != value[0]:
            return Validation.fail(['value not uppercase'])
        return Validation.success()


    def validate_contains_special_character(value):
        if re.match(r'^[a-zA-Z0-9_]*$', value):
            return Validation.fail(['value not contains special character'])
        return Validation.success()


    def validate(value):
        return (Validation.success(value)
                .ap(validate_length)
                .ap(validate_uppercase)
                .ap(validate_contains_special_character))


    validate('Success$') # Validation['Success$', []]
    validate('Success') # Validation['Success$', ['value not uppercase']]
    validate('S$') # Validation['Success$', ['value not long enough']]
    validate('s$') # Validation['Success$', ['value not long enough', 'value not uppercase']]
    validate('s') # Validation['Success$', ['value not long enough', 'value not uppercase', 'value not contains special character']]

.. autoclass:: pymonet.validation.Validation
    :members: __eq__, success, fail, is_success, is_fail, map, bind, ap, to_box, to_either, to_maybe, to_lazy, to_try