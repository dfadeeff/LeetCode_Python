import random
from typing import List


class Solution:

    def __init__(self, w: List[int]):
        """
        City Populations
        [[seattle, 500], [NY, 900], [LA, 400]]

        index -> person
        weight -> population

        :param w:
        """

        self.prefix_sum = []
        total = 0
        for weight in w:
            total += weight
            self.prefix_sum.append(total)
        self.total = total

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


if __name__ == '__main__':
    sol = Solution([1, 2, 3, 4, 5])

    # Just print a few outputs
    print(sol.pickIndex())
    print(sol.pickIndex())
    print(sol.pickIndex())
    print(sol.pickIndex())
    print(sol.pickIndex())
