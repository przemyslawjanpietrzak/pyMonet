class ImmutableList:

    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail

    @classmethod
    def on(cls, head, tail=None):
        return ImmutableList(head, tail)

    def to_list(self):
        if self.tail is None:
            return [self.head]

        return [self.head, *self.tail.to_list()]

    def append(self, new_element):
        def acc(element, head, tail):
            if tail is None:
                return ImmutableList(head, ImmutableList(element))
            return acc(
                
            )

    def unshift(self, new_elemet):
        def acc(elemet, head, tail):
            if tail is None:
                return ImmutableList(elemet, ImmutableList(head))
            return ImmutableList(elemet, acc(head, tail))

        return acc(new_elemet, self.head, self.tail)

    @property
    def length(self):
        if self.tail is None:
            return 1
        return self.tail.length + 1
