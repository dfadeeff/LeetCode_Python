from collections import defaultdict
from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        hashMap = defaultdict(list)
        for i, number in enumerate(nums):
            hashMap[number].append(i)

        for key, value in sorted(hashMap.items()):

            if len(value) > 1:
                for i in range(1, len(value)):

                    if abs(value[i] - value[i - 1]) <= k:
                        return True
        return False


if __name__ == '__main__':
    nums = [1, 2, 3, 1]
    k = 3
    print(Solution().containsNearbyDuplicate(nums, k))
    nums = [1, 0, 1, 1]
    k = 1
    print(Solution().containsNearbyDuplicate(nums, k))
