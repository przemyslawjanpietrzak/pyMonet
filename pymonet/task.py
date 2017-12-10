class Task:
    """
    Task are data-type for handle execution of functions (in lazy way)
    transform results of this function and handle errors.
    """

    def __init__(self, fork):
        """
        :param fork: function to call during fork
        :type fork: Function(reject, resolve) -> any
        """
        self.fork = fork

    @classmethod
    def of(cls, value):
        """
        :param value:
        :type value: Any
        :returns: instant resolved Task
        :rtype: Task<_, resolve>
        """
        return lambda _, resolve: resolve(value)

    @classmethod
    def reject(cls, value):
        """
        :param value:
        :type value: Any
        instant rejected Task
        :returns: Task<reject, _>
        """
        return lambda reject, _: reject(value)

    def map(self, fn):
        """
        :param fn: mapper function
        :type fn: Function(value) -> mapped_value
        :returns: Task<reject -> mapped_value>
        """
        def result(reject, resolve):
            return self.fork(
                lambda arg: reject(arg),
                lambda arg: resolve(fn(arg))
            )

        return Task(result)

    def fold(self, fn):
        """
        Also know as flatmap.

        :param fn: mapper function
        :type fn: Function(value) -> Task<reject, mapped_value>
        :returns: Task<reject, mapped_value>
        """
        def result(reject, resolve):
            return self.fork(
                lambda arg: reject(arg),
                lambda arg: fn(arg).fork(reject, resolve)
            )

        return Task(result)
