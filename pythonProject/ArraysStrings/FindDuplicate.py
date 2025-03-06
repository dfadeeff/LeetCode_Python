from collections import defaultdict

from black import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        count = defaultdict(int)
        for i in nums:
            count[i] += 1

        for k, w in count.items():
            if w > 1:
                return k

    def findDuplicate2Pointer(self, nums: List[int]) -> int:
        """The two-pointer (Floyd’s Cycle Detection) method relies on the assumption that the values in nums are valid indices in the array."""
        tortoise = hare = nums[0]
        while True:
            tortoise = nums[tortoise]
            hare = nums[nums[hare]]
            if tortoise == hare:
                break

        # Find the "entrance" to the cycle.
        tortoise = nums[0]
        while tortoise != hare:
            tortoise = nums[tortoise]
            hare = nums[hare]

        return hare


if __name__ == '__main__':
    nums = [1, 3, 4, 2, 2]
    print(Solution().findDuplicate(nums))
    # print(Solution().findDuplicate2Pointer(nums))
    nums = [2, 6, 4, 1, 3, 1, 5]
    print(Solution().findDuplicate(nums))
    # print(Solution().findDuplicate2Pointer(nums))
    nums = [1, 10000, 5, 5, 2, 6]
    print(Solution().findDuplicate(nums))
    # print(Solution().findDuplicate2Pointer(nums))
