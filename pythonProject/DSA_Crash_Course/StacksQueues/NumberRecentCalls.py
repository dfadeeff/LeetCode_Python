from collections import deque

class NumberRecentCalls:
    def __init__(self):
        self.deque = deque()

    def ping(self, t: int) -> int:
        #Evicting all calls that are too old
        while self.deque and self.deque[0] < t - 3000:
            self.deque.popleft()

        self.deque.append(t)
        return len(self.deque)


if __name__ == '__main__':
    recent_counter = NumberRecentCalls()
    # Test the pings as given in the example
    print(recent_counter.ping(1))  # requests = [1], range is [-2999,1], should return 1
    print(recent_counter.ping(100))  # requests = [1, 100], range is [-2900,100], should return 2
    print(recent_counter.ping(3001))  # requests = [1, 100, 3001], range is [1,3001], should return 3
    print(recent_counter.ping(3002))  # requests = [1, 100, 3001, 3002], range is [2,3002], should return 3
    print(recent_counter.ping(4000))  # requests = [1, 100, 3001, 3002], range is [2,3002], should return 3