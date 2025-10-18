from collections import defaultdict


class Solution:
    def intersection(self, nums):
        counts = defaultdict(int)
        for arr in nums:
            for x in arr:
                counts[x] += 1

        print(counts)
        n = len(nums)
        ans = []
        for key in counts:
            if counts[key] == n:
                ans.append(key)
        return ans


if __name__ == "__main__":
    nums = [[3, 1, 2, 4, 5], [1, 2, 3, 4], [3, 4, 5, 6]]
    print(Solution().intersection(nums))
