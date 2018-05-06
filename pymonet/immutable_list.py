class ImmutableList:

    def __init__(self, head=None, tail=None, is_empty=False):
        self.head = head
        self.tail = tail
        self.is_empty = is_empty

    def __eq__(self, other):
        return isinstance(other, ImmutableList) \
            and self.head == other.head\
            and self.tail == other.tail\
            and self.is_empty == other.is_empty

    def __str__(self):
        return 'ImmutableList{}'.format(self.to_list())

    def __add__(self, other):
        if not isinstance(other, ImmutableList):
            raise ValueError()
        
        if self.tail is None:
            return ImmutableList(self.head, other)
        
        return ImmutableList(
            self.head,
            self.tail.__add__(other)
        )

    @classmethod
    def of(cls, head, *elements):
        if len(elements) == 0:
            return ImmutableList(head)
        return ImmutableList(
            head,
            ImmutableList.of(elements[0], *elements[1:])
        )

    @classmethod
    def empty(cls):
        return ImmutableList(is_empty=True)

    @property
    def length(self):
        if self.tail is None:
            return 1

        return self.tail.length + 1

    def to_list(self):
        if self.tail is None:
            return [self.head]

        return [self.head, *self.tail.to_list()]

    def append(self, new_element):
        def acc(elemet, head, tail):
            if tail is None:
                return ImmutableList(head, ImmutableList(elemet))

            return ImmutableList(elemet, acc(head, tail))

        return acc(new_element, self.head, self.tail)

    def unshift(self, new_elemet):
        def acc(elemet, head, tail):
            if tail is None:
                return ImmutableList(elemet, ImmutableList(head))

            return ImmutableList(elemet, acc(head, tail))

        return acc(new_elemet, self.head, self.tail)

    def map(self, fn):
        if self.tail is None:
            return ImmutableList(fn(self.head))

        return ImmutableList(fn(self.head), self.tail.map(fn))

    def filter(self, fn):
        if self.tail is None:
            if fn(self.head):
                return ImmutableList(self.head)
            return ImmutableList(is_empty=True)

        if fn(self.head):
            return ImmutableList(self.head, self.tail.filter(fn))

        return self.tail.filter(fn)

    def find(self, fn):
        if self.tail is None:
            return self.head if fn(self.head) else None
        
        if fn(self.head):
            return self.head

        return self.tail.find(fn)

