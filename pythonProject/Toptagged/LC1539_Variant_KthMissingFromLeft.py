from typing import List


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        left, right = 0, len(arr) - 1
        while left <= right:
            pivot = (left + right) // 2
            # If number of positive integers
            # which are missing before arr[pivot]
            # is less than k -->
            # continue to search on the right.
            missing = arr[pivot] - (pivot + arr[0])
            if missing < k:
                left = pivot + 1
            # Otherwise, go left.
            else:
                right = pivot - 1

        # At the end of the loop, left = right + 1,
        # and the kth missing is in-between arr[right] and arr[left].
        # The number of integers missing before arr[right] is
        # arr[right] - right - 1 -->
        # the number to return is
        # arr[right] + k - (arr[right] - right - 1) = k + left
        return k + arr[0] + (left-1)


if __name__ == "__main__":
    arr = [4, 7, 8, 10]
    k = 1
    print(Solution().findKthPositive(arr, k))
    arr = [4, 7, 9, 10]
    k = 3
    print(Solution().findKthPositive(arr, k))
    arr = [1, 2, 4]
    k = 3
    print(Solution().findKthPositive(arr, k))
