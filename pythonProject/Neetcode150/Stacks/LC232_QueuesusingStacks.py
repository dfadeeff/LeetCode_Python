class MyQueue:

    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def push(self, x: int) -> None:
        self.stack1.append(x)

    def pop(self) -> int:
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())

        return self.stack2.pop()

    def peek(self) -> int:
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())

        return self.stack2[-1]

    def empty(self) -> bool:
        return len(self.stack1) == 0 and len(self.stack2) == 0


if __name__ == "__main__":
    s = MyQueue()

    s.push(1)
    s.push(2)
    s.peek()
    s.pop()
    s.empty()

    print(s.peek())  # should print 2
    print(s.pop())  # should print 2
    print(s.empty())  # should print False
