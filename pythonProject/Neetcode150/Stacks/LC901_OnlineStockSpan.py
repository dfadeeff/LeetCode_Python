from collections import deque


class StockSpanner:

    def __init__(self):
        self.deque = deque()

    def next(self, price: int) -> int:
        span = 1
        while self.deque and self.deque[-1][0] <= price:
            span += self.deque.pop()[1]

        self.deque.append([price, span])

        return span

if __name__ == "__main__":
    obj = StockSpanner()
    print(obj.next(100))
    print(obj.next(80))
    print(obj.next(60))
    print(obj.next(70))
    print(obj.next(60))
    print(obj.next(75))
    print(obj.next(85))

