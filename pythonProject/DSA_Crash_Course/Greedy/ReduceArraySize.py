from collections import Counter
from typing import List


class Solution:
    def minSetSize(self, arr: List[int]) -> int:
        counter = Counter(arr)
        n = len(arr)
        ordered = sorted(counter.values(), reverse=True)
        ans = 0
        sum = 0
        for i in ordered:
            sum += i
            if sum >= n / 2:
                break
            ans += 1

        return ans + 1


def main():
    arr = [3, 3, 3, 3, 5, 5, 5, 2, 2, 7]
    print(Solution().minSetSize(arr))
    arr = [7, 7, 7, 7, 7, 7]
    print(Solution().minSetSize(arr))


if __name__ == '__main__':
    main()
