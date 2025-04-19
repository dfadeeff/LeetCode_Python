from typing import List


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        left = 0
        right = len(arr) - 1


        # If you used <, you’d exit before ever testing that last index, and you could be off by one.
        while left <= right:
            pivot = (left + right) // 2
            missing = arr[pivot] - (pivot+1)
            if missing >= k:
                right = pivot - 1
            else:
                left = pivot + 1

        return left + k


if __name__ == "__main__":
    arr = [2, 3, 4, 7, 11]
    k = 5
    print(Solution().findKthPositive(arr, k))
