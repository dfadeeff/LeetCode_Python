from typing import List


class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        # pick smaller one
        if len(arr1) > len(arr2):
            arr1, arr2 = arr2, arr1

        prefix_set = set()
        for n in arr1:
            while n:
                prefix_set.add(n)
                n = n // 10
        res = 0
        for n in arr2:
            while n and n not in prefix_set:
                n = n // 10

            if n in prefix_set:
                res = max(res, len(str(n)))

        return res


if __name__ == "__main__":
    arr1 = [1, 10, 100]
    arr2 = [1000]
    print(Solution().longestCommonPrefix(arr1, arr2))
