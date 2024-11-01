from typing import List
from collections import Counter


class Solution:
    def findLeastNumOfUniqueInts(self, arr: List[int], k: int) -> int:
        # remove elements with the lowest frequency to maximize removals
        counter = Counter(arr)
        ordered = sorted(counter.values(), reverse=True)

        while k:
            val = ordered[-1]
            if val <= k:
                k -= val
                ordered.pop()

            else:
                break
        return len(ordered)


def main():
    arr = [5, 5, 4]
    k = 1
    print(Solution().findLeastNumOfUniqueInts(arr, k))
    arr = [4, 3, 1, 1, 3, 3, 2]
    k = 3
    print(Solution().findLeastNumOfUniqueInts(arr, k))


if __name__ == '__main__':
    main()
