from collections import Counter
from typing import List


class Solution:
    def smallestCommonElement(self, mat: List[List[int]]) -> int:
        counter = Counter()

        for row in mat:
            # Only count unique elements in each row to avoid over-counting
            counter.update(set(row))
        print(counter)
        rows = len(mat)

        for num in sorted(counter):  # Sorted to get the smallest first
            if counter[num] == rows:
                return num

        return -1


if __name__ == '__main__':
    mat = [[1, 2, 3, 4, 5], [2, 4, 5, 8, 10], [3, 5, 7, 9, 11], [1, 3, 5, 7, 9]]
    print(Solution().smallestCommonElement(mat))
