class Task:

    def __init__(self, fork):
        """
        :param fork: function to call during fork
         :type: (reject, resolve) -> any
        """
        self.fork = fork

    @classmethod
    def of(cls, value):
        """
        :param value
        :type: any
        instant rejected Task
        :return: Task<_, resolve>
        """
        return lambda _, resolve: resolve(value)

    @classmethod
    def reject(cls, value):
        """
        :param value
        :type: any
        instant rejected Task
        :return: Task<reject, _>
        """
        return lambda reject, _: reject(value)

    def map(self, fn):
        """
        :param fn: mapper function
        :type fn: value -> mapped_value
        :return: Task<reject -> mapped_value>
        """
        def result(reject, resolve):
            return self.fork(
                lambda arg: reject(arg),
                lambda arg: resolve(fn(arg))
            )

        return Task(result)

    def fold(self, fn):
        """
        also know as flatmap
        :param fn: mapper function
        :type fn: value -> Task<reject, mapped_value>
        :return: Task<reject, mapped_value>
        """
        def result(reject, resolve):
            return self.fork(
                lambda arg: reject(arg),
                lambda arg: fn(arg).fork(reject, resolve)
            )

        return Task(result)
