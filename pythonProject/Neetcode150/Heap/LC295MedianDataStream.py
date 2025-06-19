import heapq


class MedianFinder:

    def __init__(self):
        self.small, self.large = [], []

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)  # map heap, by default

        # make sure every num small s <= every num in large
        if (self.small and self.large and -self.small[0] > self.large[0]):
            val = - heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # uneven size
        if len(self.small) > len(self.large) + 1:
            val = - heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        if len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]

        return (-self.small[0] + self.large[0]) / 2

if __name__ == "__main__":
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5, "Test Case 1 Failed"

    mf.addNum(3)
    assert mf.findMedian() == 2.0, "Test Case 2 Failed"

    mf.addNum(4)
    assert mf.findMedian() == 2.5, "Test Case 3 Failed"

    mf2 = MedianFinder()
    mf2.addNum(5)
    assert mf2.findMedian() == 5.0, "Test Case 4 Failed"

    print("All test cases passed!")
