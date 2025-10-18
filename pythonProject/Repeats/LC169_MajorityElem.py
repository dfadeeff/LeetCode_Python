from collections import defaultdict


class Solution:

    def majorityElem(self, nums):
        freq = defaultdict(int)
        for i in nums:
            freq[i] += 1

        inv_map = {v: k for k, v in freq.items()}
        max_key = 0
        for k, v in inv_map.items():
            max_key = max(k, max_key)

        return inv_map[max_key]


if __name__ == "__main__":
    nums = [3, 2, 3]
    print(Solution().majorityElem(nums))
