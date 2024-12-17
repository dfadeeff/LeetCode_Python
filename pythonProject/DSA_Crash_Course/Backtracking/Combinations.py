from typing import List


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def backtrack(curr, i):
            if len(curr) == k:
                ans.append(curr[:])
                return

            for num in range(i, n + 1):
                curr.append(num)
                backtrack(curr, num + 1)
                curr.pop()

        ans = []
        backtrack([], 1)

        return ans


def main():
    n = 4
    k = 2
    print(Solution().combine(n, k))
    n = 1
    k = 1
    print(Solution().combine(n, k))

if __name__ == '__main__':
    main()