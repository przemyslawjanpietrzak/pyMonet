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
        :return: Task<_ -> value>
        """
        def result(_, resolve):
            return resolve(value)

        return result

    @classmethod
    def reject(cls, value):
        """
        :param value
        :type: any
        instant rejected Task
        :return: Task<_ -> value>
        """
        def result(reject, _):
            return reject(value)

        return result

    def map(self, fn):
        """
        :param fn: mapper function
        :type fn: value -> other_value
        :return: Task<_ -> other_value>
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
        :type fn: value -> Task<other_value>
        :return: Task<_ -> other_value>
        """
        def result(reject, resolve):
            return self.fork(
                lambda arg: reject(arg),
                lambda arg: fn(arg).fork(reject, resolve)
            )

        return Task(result)
