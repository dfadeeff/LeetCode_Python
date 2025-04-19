from typing import List

from black.trans import defaultdict


class Solution:
    def countPairs(self, nums: List[int], k: int) -> int:
        freq = defaultdict(list)
        count = 0
        for i in range(len(nums)):
            freq[nums[i]].append(i)
        # print(freq)
        for v in freq.values():
            for j in range(len(v)):
                for z in range(j + 1, len(v)):
                    if v[j] * v[z] % k == 0:
                        count += 1
        return count


if __name__ == "__main__":
    nums = [3, 1, 2, 2, 2, 1, 3]
    k = 2
    print(Solution().countPairs(nums, k))
