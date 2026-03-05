from collections import deque


class HitCounter:

    def __init__(self):
        self.queue = deque()

    def hit(self, timestamp: int) -> None:
        self.queue.append(timestamp)

    def getHits(self, timestamp: int) -> int:
        # Remove hits older than 300 seconds
        while self.queue and self.queue[0] <= timestamp - 300:
            self.queue.popleft()
        return len(self.queue)


class HitCounterCircularBuffer:
    """Design a hit counter which counts the number of hits received in the past 5 minutes (i.e., the past 300 seconds)."""

    def __init__(self):
        self.times = [0] * 300  # which timestamp last wrote to this slot
        self.hits = [0] * 300  # how many hits at that timestamp

    def hit(self, timestamp: int) -> None:
        index = timestamp % 300
        if self.times[index] != timestamp:
            # New timestamp in this slot → reset
            self.times[index] = timestamp
            self.hits[index] = 1
        else:
            # Same timestamp → add to count
            self.hits[index] += 1

    def getHits(self, timestamp: int) -> int:
        total = 0
        for i in range(300):
            # Only count if the hit is within the last 300 seconds
            if timestamp - self.times[i] < 300:
                total += self.hits[i]
        return total


if __name__ == "__main__":
    print("Brute force method")
    sol = HitCounter()
    sol.hit(1)
    sol.hit(2)
    sol.hit(3)
    print(sol.getHits(4))
    sol.hit(300)
    print(sol.getHits(300))
    print(sol.getHits(301))
    print("Circular buffer method")
    sol = HitCounterCircularBuffer()
    sol.hit(1)
    sol.hit(2)
    sol.hit(3)
    print(sol.getHits(4))
    sol.hit(300)
    print(sol.getHits(300))
    print(sol.getHits(301))
