from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if len(nums) == 1 and nums[0] != target:
            return -1

        min_element = min(nums)
        position = nums.index(min_element)
        print("position", position)

        nums.sort()
        print(nums)
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return (mid + position) % len(nums)
            elif nums[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return -1


if __name__ == "__main__":
    nums = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    print(Solution().search(nums, target))
    nums = [4, 5, 6, 7, 0, 1, 2]
    target = 3
    print(Solution().search(nums, target))
    nums = [1]
    target = 0
    print(Solution().search(nums, target))
    nums = [3, 1]
    target = 3
    print(Solution().search(nums, target))
