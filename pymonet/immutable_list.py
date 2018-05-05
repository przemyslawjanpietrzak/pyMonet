class ImmutableList:

    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail

    def __eq__(self, other):
        return isinstance(other, ImmutableList) \
            and self.head == other.head\
            and self.tail == self.tail

    @classmethod
    def of(cls, head, *elements):
        if len(elements) == 0:
            return ImmutableList(head)
        return ImmutableList(
            head,
            ImmutableList.of(elements[0], *elements[1:])
        )

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
        if fn(self.head):
            return self.tail.filter(fn).unshift(self.head)
        return self.tail.filter(fn)
