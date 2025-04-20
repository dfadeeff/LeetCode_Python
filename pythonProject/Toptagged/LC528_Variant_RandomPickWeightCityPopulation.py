import random
from typing import List


class Solution:

    def __init__(self, city_populations: List[int]):
        self.prefix_sum = []
        self.cities = []
        total = 0
        for name, pop in city_populations:
            self.cities.append(name)
            total += pop
            self.prefix_sum.append(total)
        self.total = total
        print("prefix_sum:", self.prefix_sum)
        print("cities:", self.cities)

    def pickCity(self) -> int:
        """
        [1,2,4] -> 0 [ 1, 3, 7] prepend 0, if we get 4 it should find a range with binary search
        :return:
        """
        target = random.uniform(0, self.total)
        l = 0
        r = len(self.prefix_sum)  # dealing with an index, not inclusive at the end!
        while l < r:
            mid = (l + r) // 2
            if self.prefix_sum[mid] < target:
                l = mid + 1
            else:
                r = mid

        return self.cities[l]


# Your Solution object will be instantiated and called as such:
# obj = Solution(w)
# param_1 = obj.pickIndex()

if __name__ == "__main__":
    cities = [
        ["Seattle", 500],
        ["New York", 900],
        ["Los Angeles", 400]
    ]

    sol = Solution(cities)

    print("Random city picks (proportional to population):")
    for _ in range(10):  # Try a few times to observe randomness
        print(sol.pickCity(), end=' ')
