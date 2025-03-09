from typing import List

from black.trans import defaultdict


class Solution:
    def countElements(self, arr: List[int]) -> int:
        hashMap = defaultdict(int)
        for i in arr:
            hashMap[i] += 1

        num_elements = 0
        for i in arr:
            if (i + 1) in hashMap.keys():
                num_elements += 1
        return num_elements


if __name__ == '__main__':
    arr = [1, 2, 3]
    print(Solution().countElements(arr))
    arr = [1, 1, 3, 3, 5, 5, 7, 7]
    print(Solution().countElements(arr))
    arr = [1, 3, 2, 3, 5, 0]
    print(Solution().countElements(arr))
