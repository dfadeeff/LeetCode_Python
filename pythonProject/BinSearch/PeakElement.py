from typing import List


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return nums[0]
        for i in range(len(nums)):
            if i == 0 and nums[i] > nums[i + 1]:
                return i
                break
            elif i == len(nums) - 1 and nums[i] > nums[i - 1]:
                return i
                break
            else :
                if nums[i] > nums[i + 1] and nums[i] > nums[i - 1]:
                    return i
                    break

        return -1


if __name__ == '__main__':
    nums = [1, 2, 3, 1]
    print(Solution().findPeakElement(nums))
    nums = [1,2,1,3,5,6,4]
    print(Solution().findPeakElement(nums))
