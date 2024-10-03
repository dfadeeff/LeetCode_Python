from collections import deque


class MADAtaStream:

    def __init__(self, size: int):
        self.size = size
        self.deque = deque()

    def next(self, val: int) -> float:
        sum = 0
        average = 0
        while self.deque and len(self.deque) >= self.size:
            self.deque.popleft()

        self.deque.append(val)

        for i in range(len(self.deque)):
            sum += self.deque[i]
            average = sum / len(self.deque)

        return average


if __name__ == '__main__':
    average_stream = MADAtaStream(3)
    # Test the pings as given in the example
    print(average_stream.next(1))
    print(average_stream.next(10))
    print(average_stream.next(3))
    print(average_stream.next(5))
