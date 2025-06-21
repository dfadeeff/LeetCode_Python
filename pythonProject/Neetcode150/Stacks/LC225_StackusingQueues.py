from collections import deque


class MyStack:

    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)

    def pop(self) -> int:
        for _ in range(len(self.q) - 1):
            self.push(self.q.popleft())  # move from left of the queue to the right of the queue
        return self.q.popleft()

    def top(self) -> int:
        return self.q[-1]

    def empty(self) -> bool:
        return len(self.q) == 0


if __name__ == "__main__":
    s = MyStack()

    s.push(1)
    s.push(2)

    print(s.top())  # should print 2
    print(s.pop())  # should print 2
    print(s.empty())  # should print False
