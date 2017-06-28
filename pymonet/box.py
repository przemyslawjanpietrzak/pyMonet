class Box:
    """
    Data type for storage any type of data
    """

    def __init__(self, value):
        """
        :param value: value to store in Box
        :type any
        """
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def map(self, fn):
        """
        takes function (a) -> b and applied this function on current box value and returns new box with mapped value
        :param fn: mapper function
        :type (a) -> b
        :return: new box with mapped value
        :type Box<b>
        """
        return Box(fn(self.value))

    def fold(self, fn):
        """
        takes function (a) -> b and applied this function on current box value and returns mapped value
        :param fn: mapper function
        :type (a) -> b
        :return: new box with mapped value
        :type b
        """
        return fn(self.value)
