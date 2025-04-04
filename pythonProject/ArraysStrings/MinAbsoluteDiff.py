from typing import List


class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()

        lists = []
        min_diff = float('inf')
        for i in range(1, len(arr)):
            min_diff = min(min_diff, abs(arr[i] - arr[i - 1]))
        for i in range(1, len(arr)):
            if abs(arr[i - 1] - arr[i]) == min_diff:
                lists.append([arr[i-1], arr[i]])
        return lists


if __name__ == '__main__':
    arr = [4, 2, 1, 3]
    print(Solution().minimumAbsDifference(arr))
    arr = [1, 3, 6, 10, 15]
    print(Solution().minimumAbsDifference(arr))
