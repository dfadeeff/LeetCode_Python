from collections import defaultdict
import random
from typing import List


class Solution:
    """In this approach, we pre-compute the indices for each unique number in the array. During initialization, we traverse the array and store a list of positions (indices) for each number in a dictionary. This way, when the pick method is called with a target value, we simply look up its list of indices and return one of them at random. While this method makes the pick operation efficient, it comes at the cost of extra space since we store all the indices for each number."""

    def __init__(self, nums: List[int]):
        self.indices = defaultdict(list)
        for i, num in enumerate(nums):
            self.indices[num].append(i)
        print(self.indices)

    def pick(self, target: int) -> int:
        return random.choice(self.indices[target])


if __name__ == "__main__":
    nums = [1, 2, 3, 3, 3]
    solution = Solution(nums)
    target = 3
    print(solution.pick(target))  # Randomly picks one of the indices where 3 is present.
