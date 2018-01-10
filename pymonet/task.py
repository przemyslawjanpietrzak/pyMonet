class Task:
    """
    Task are data-type for handle execution of functions (in lazy way)
    transform results of this function and handle errors.
    """

    def __init__(self, fork):
        """
        :param fork: function to call during fork
        :type fork: Function(reject, resolve) -> Any
        """
        self.fork = fork

    @classmethod
    def of(cls, value):
        """
        Return resolved Task with stored value argument.

        :param value: value to store in Task
        :type value: A
        :returns: resolved Task
        :rtype: Task[Function(_, resolve) -> A]
        """
        return Task(lambda _, resolve: resolve(value))

    @classmethod
    def reject(cls, value):
        """
        Return rejected Task with stored value argument.

        :param value: value to store in Task
        :type value: A
        :returns: rejected Task
        :rtype: Task[Function(reject, _) -> A]
        """
        return Task(lambda reject, _: reject(value))

    def map(self, fn):
        """
        Take function, store it and call with Task value during calling fork function.
        Return new Task with result of called.

        :param fn: mapper function
        :type fn: Function(value) -> B
        :returns: new Task with mapped resolve attribute
        :rtype: Task[Function(resolve, reject -> A | B]
        """
        def result(reject, resolve):
            return self.fork(
                lambda arg: reject(arg),
                lambda arg: resolve(fn(arg))
            )

        return Task(result)

    def bind(self, fn):
        """
        Take function, store it and call with Task value during calling fork function.
        Return result of called.

        :param fn: mapper function
        :type fn: Function(value) -> Task[reject, mapped_value]
        :returns:  new Task with mapper resolve attribute
        :rtype: Task[reject, mapped_value]
        """
        def result(reject, resolve):
            return self.fork(
                lambda arg: reject(arg),
                lambda arg: fn(arg).fork(reject, resolve)
            )

        return Task(result)
