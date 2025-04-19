from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k= 0
        for i in range(len(nums)):
            if nums[i] != val:
                # partition in quick select
                nums[k] = nums[i]
                k += 1
        return k


if __name__ == "__main__":
    nums = [3, 2, 2, 3]
    val = 3
    print(Solution().removeElement(nums, val))
