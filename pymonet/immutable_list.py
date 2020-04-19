from typing import TypeVar, Generic, Callable, Optional


T = TypeVar('T')
U = TypeVar('U')


class ImmutableList(Generic[T]):
    """
    Immutable list is data structure that doesn't allow to mutate instances
    """

    def __init__(self, head: T = None, tail: 'ImmutableList[T]' = None, is_empty: bool = False) -> None:
        self.head = head
        self.tail = tail
        self.is_empty = is_empty

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ImmutableList) \
            and self.head == other.head\
            and self.tail == other.tail\
            and self.is_empty == other.is_empty

    def __str__(self) -> str:  # pragma: no cover
        return 'ImmutableList{}'.format(self.to_list())

    def __add__(self, other: 'ImmutableList[T]') -> 'ImmutableList[T]':
        """
        If Maybe is empty return new empty Maybe, in other case
        takes mapper function and returns result of mapper.

        :param mapper: function to call with Maybe.value
        :type mapper: Function(A) -> Maybe[B]
        :returns: Maybe[B | None]
        """
        if not isinstance(other, ImmutableList):
            raise ValueError('ImmutableList: you can not add any other instace than ImmutableList')

        if self.tail is None:
            return ImmutableList(self.head, other)

        return ImmutableList(
            self.head,
            self.tail.__add__(other)
        )

    def __len__(self):
        if self.head is None:
            return 0

        if self.tail is None:
            return 1

        return len(self.tail) + 1

    @classmethod
    def of(cls, head: T, *elements) -> 'ImmutableList[T]':
        if len(elements) == 0:
            return ImmutableList(head)

        return ImmutableList(
            head,
            ImmutableList.of(elements[0], *elements[1:])
        )

    @classmethod
    def empty(cls):
        return ImmutableList(is_empty=True)


    def to_list(self):
        if self.tail is None:
            return [self.head]

        return [self.head, *self.tail.to_list()]

    def append(self, new_element: T) -> 'ImmutableList[T]':
        """
        Returns new ImmutableList with elements from previous one
        and argument value on the end of list

        :param new_element: element to append on the end of list
        :type fn: A
        :returns: ImmutableList[A]
        """
        return self + ImmutableList(new_element)

    def unshift(self, new_element: T) -> 'ImmutableList[T]':
        """
        Returns new ImmutableList with argument value on the begin of list
        and other list elements after it

        :param new_element: element to append on the begin of list
        :type fn: A
        :returns: ImmutableList[A]
        """
        return ImmutableList(new_element) + self

    def map(self, fn: Callable[[Optional[T]], U]) -> 'ImmutableList[U]':
        """
        Returns new ImmutableList with each element mapped into
        result of argument called with each element of ImmutableList

        :param fn: function to call with ImmutableList value
        :type fn: Function(A) -> B
        :returns: ImmutableList[B]
        """
        if self.tail is None:
            return ImmutableList(fn(self.head))

        return ImmutableList(fn(self.head), self.tail.map(fn))

    def filter(self, fn: Callable[[Optional[T]], bool]) -> 'ImmutableList[T]':
        """
        Returns new ImmutableList with only this elements that passed
        info argument returns True

        :param fn: function to call with ImmutableList value
        :type fn: Function(A) -> bool
        :returns: ImmutableList[A]
        """
        if self.tail is None:
            if fn(self.head):
                return ImmutableList(self.head)
            return ImmutableList(is_empty=True)

        if fn(self.head):
            return ImmutableList(self.head, self.tail.filter(fn))

        return self.tail.filter(fn)

    def find(self, fn: Callable[[Optional[T]], bool]) -> Optional[T]:
        """
        Returns first element of ImmutableList that passed
        info argument returns True

        :param fn: function to call with ImmutableList value
        :type fn: Function(A) -> bool
        :returns: A
        """
        if self.head is None:
            return None

        if self.tail is None:
            return self.head if fn(self.head) else None

        if fn(self.head):
            return self.head

        return self.tail.find(fn)

    def reduce(self, fn: Callable[[U, T], U], acc: U) -> U:
        """
        Method executes a reducer function
        on each element of the array, resulting in a single output value.

        :param fn: function to call with ImmutableList value
        :type fn: Function(A, B) -> A
        :returns: A
        """
        if self.head is None:
            return acc

        if self.tail is None:
            return fn(self.head, acc)

        
        return self.tail.reduce(fn, fn(acc, self.head))