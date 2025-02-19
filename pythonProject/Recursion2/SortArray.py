from typing import List


class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) < 2:
            return nums

        pivot = int(len(nums) / 2)
        left_list = self.sortArray(nums[0:pivot])
        right_list = self.sortArray(nums[pivot:])
        return self.merge_sort(left_list, right_list)

    def merge_sort(self, left_list: List[int], right_list: List[int]) -> List[int]:
        left_cursor = right_cursor = 0
        ret = []
        while left_cursor < len(left_list) and right_cursor < len(right_list):
            if left_list[left_cursor] < right_list[right_cursor]:
                ret.append(left_list[left_cursor])
                left_cursor += 1
            else:
                ret.append(right_list[right_cursor])
                right_cursor += 1

        # append what is remained in either of the lists
        ret.extend(left_list[left_cursor:])
        ret.extend(right_list[right_cursor:])

        return ret


if __name__ == '__main__':
    nums = [5, 2, 3, 1]
    print(Solution().sortArray(nums))