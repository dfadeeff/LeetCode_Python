import random
from typing import List


class Solution:

    def __init__(self, w: List[int]):
        self.prefix_sum = []
        total = 0
        for weight in w:
            total += weight
            self.prefix_sum.append(total)
        self.total = total
        print("prefix_sum", self.prefix_sum)
        print("total", self.total)

    def pickIndex(self) -> int:
        """
        [1,2,4] -> 0 [ 1, 3, 7] prepend 0, if we get 4 it should find a range with binary search
        :return:
        """
        target = random.uniform(0, self.total)
        l = 0
        r = len(self.prefix_sum)  # dealing with an index
        while l < r:
            mid = (l + r) // 2
            if self.prefix_sum[mid] < target:
                l = mid + 1
            else:
                r = mid

        return l


# Your Solution object will be instantiated and called as such:
# obj = Solution(w)
# param_1 = obj.pickIndex()

if __name__ == "__main__":
    w = [1, 3]
    sol = Solution(w)

    print("Random picks (should be 0 ~25% and 1 ~75%):")
    for _ in range(10):  # Try a few times to observe randomness
        print(sol.pickIndex(), end=' ')
