from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in range(len(matrix)):
            if self.binarySearch(matrix[row], target):
                return True
        return False


    def binarySearch(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2
            pivot = nums[mid]
            if pivot == target:
                return True
            elif target < pivot:
                right = mid - 1
            elif target > pivot:
                left = mid + 1
        return False



if __name__ == '__main__':
    matrix = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24],
              [18, 21, 23, 26, 30]]
    target = 5
    print(Solution().searchMatrix(matrix, target))
    matrix = [[1, 1]]
    target = 0
    print(Solution().searchMatrix(matrix, target))
