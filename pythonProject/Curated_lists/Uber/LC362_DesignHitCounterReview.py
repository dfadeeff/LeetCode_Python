from collections import deque


class HitCounter:
    """
    hit(timestamp)    → record a hit at this time
    getHits(timestamp)→ how many hits in last 300 seconds?
                    i.e. [timestamp-299, timestamp]



    Only care about 300 second window
    Old hits → irrelevant → remove them

    deque = naturally ordered by time
      append new hits at back
      remove old hits from front

    Same timestamp → (timestamp, count) not one entry per hit


    hit(1):   deque=[(1,1)]
    hit(1):   deque=[(1,2)]    ← same timestamp, increment count
    hit(2):   deque=[(1,2),(2,1)]
    hit(3):   deque=[(1,2),(2,1),(3,1)]
    """

    def __init__(self):
        self.hits = deque()  # (timestamp, count)

    def hit(self, timestamp: int) -> None:
        if self.hits and self.hits[-1][0] == timestamp:
            # same second → just increment
            t, c = self.hits.pop()
            self.hits.append((t, c + 1))
        else:
            self.hits.append((timestamp, 1))

    def getHits(self, timestamp: int) -> int:
        # Remove hits older than 300 seconds
        while self.hits and self.hits[0][0] <= timestamp - 300:
            self.hits.popleft()
        return sum(c for t, c in self.hits)


if __name__ == "__main__":
    hc = HitCounter()
    hc.hit(1)
    hc.hit(1)
    hc.hit(2)
    hc.hit(3)
    print(hc.getHits(4))  # 4
    hc.hit(300)
    print(hc.getHits(300))   # 5
    print(hc.getHits(301))   # 3  ← timestamp 1 expired
    print(hc.getHits(400))   # 1  ← only timestamp 300 remains
