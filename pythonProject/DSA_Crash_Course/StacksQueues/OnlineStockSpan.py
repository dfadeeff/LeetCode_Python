from collections import deque


class OnlineStockSpan:
    def __init__(self):
        self.deque = deque()

    def next(self, price: int) -> int:
        span = 1
        while self.deque and self.deque[-1][0] <= price:
            span += self.deque.pop()[1]

        self.deque.append((price, span))

        return span


    def nextSeparateSpanDeque(self, price: int) -> int:
        span = 1
        while self.deque and self.deque[-1] <= price:
            self.deque.pop()
            span += 1

        self.deque.append(price)

        return span


if __name__ == '__main__':
    stockspan = OnlineStockSpan()
    # Test the pings as given in the example
    print(stockspan.next(100))
    print(stockspan.next(80))
    print(stockspan.next(60))
    print(stockspan.next(70))
    print(stockspan.next(60))
    print(stockspan.next(75))
    print(stockspan.next(85))
