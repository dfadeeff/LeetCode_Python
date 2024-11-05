from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        flattened_matrix = [element for row in matrix for element in row]

        left = 0
        right = len(flattened_matrix) - 1
        while left <= right:
            mid = (left + right) // 2
            if flattened_matrix[mid] == target:
                return True
            if flattened_matrix[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return False


def main():
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    target = 3
    print(Solution().searchMatrix(matrix, target))
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    target = 13
    print(Solution().searchMatrix(matrix, target))


if __name__ == '__main__':
    main()
