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

    def map(self, mapper):
        """
        takes function (a) -> b and applied this function on current box value and returns new box with mapped value
        :param mapper: mapper function
        :type (a) -> b
        :return: new box with mapped value
        :type Box<b>
        """
        return Box(mapper(self.value))

    def bind(self, mapper):
        """
        takes function (a) -> b and applied this function on current box value and returns mapped value
        :param mapper: mapper function
        :type (a) -> b
        :return: new box with mapped value
        :type b
        """
        return mapper(self.value)

    def ap(self, monad):
        """
        It takes as a parameter another Box type which contains a function,
        and then applies that function to the value contained in the calling Box.
        :param monad: monad contains function
        :type Box[A -> B]
        :return: new Box with result of contains function
        :type Box[B]
        """
        return self.map(monad.value)
