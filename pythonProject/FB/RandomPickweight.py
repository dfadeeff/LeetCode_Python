import random
from typing import List, Tuple


class Solution:

    def __init__(self, city_populations: List[Tuple[str, int]]):
        self.prefix_sum = []
        self.cities = []
        total = 0

        for city, population in city_populations:
            total += population
            self.prefix_sum.append(total)
            self.cities.append(city)
        self.total = total

    def pickIndex(self) -> int:
        """
        [1,2,4] -> 0 [ 1, 3, 7] prepend 0, if we get 4 it should find a range with binary search
        :return:
        """
        target = random.uniform(0, self.total)
        # Binary search to find the city
        left, right = 0, len(self.prefix_sum) - 1
        while left < right:
            mid = (left + right) // 2
            if self.prefix_sum[mid] < target:
                left = mid + 1
            else:
                right = mid

        return self.cities[left]


if __name__ == '__main__':
    picker = Solution([["Seattle", 500], ["New York", 900], ["Los Angeles", 400]])

    # Print random picks!
    print(picker.pickIndex())
    print(picker.pickIndex())
    print(picker.pickIndex())
    print(picker.pickIndex())
