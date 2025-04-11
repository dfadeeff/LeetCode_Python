from collections import deque


class MovingAverage:

    def __init__(self, size: int):
        self.size = size
        self.window = deque()
        self.window_sum = 0

    def next(self, val: int) -> float:
        self.window.append(val)
        self.window_sum += val

        if len(self.window) > self.size:
            removed = self.window.popleft()
            self.window_sum -= removed
        return self.window_sum / len(self.window)


if __name__ == '__main__':
    moving_average = MovingAverage(3)

    print(moving_average.next(1))  # Output: 1.0
    print(moving_average.next(10))  # Output: (1 + 10) / 2 = 5.5
    print(moving_average.next(3))  # Output: (1 + 10 + 3) / 3 = 4.66667
    print(moving_average.next(5))  # Output: (10 + 3 + 5) / 3 = 6.0
