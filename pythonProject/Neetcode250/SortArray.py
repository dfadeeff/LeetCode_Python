from typing import List


class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums
        n = len(nums)
        mid = n // 2
        left = self.sortArray(nums[:mid])
        right = self.sortArray(nums[mid:])

        return self.merge(left, right)

    def merge(self, left_part, right_part):
        result = []
        i, j = 0, 0
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                result.append(left_part[i])
                i += 1
            else:
                result.append(right_part[j])
                j += 1
        result.extend(left_part[i:])
        result.extend(right_part[j:])
        return result


if __name__ == "__main__":
    sol = Solution()
    nums = [10, 9, 1, 1, 1, 2, 3, 1]
    print(sol.sortArray(nums))
