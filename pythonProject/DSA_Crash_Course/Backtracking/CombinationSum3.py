from typing import List


class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        results = []

        def backtrack(start, remaining, path):
            """

            :param start: From which number we are allowed to pick next.
            :param remaining: How much more we need to add to reach n.
            :param path: The current combination of chosen numbers.
            :return:
            """
            # If we have chosen k numbers
            if len(path) == k and remaining == 0:
                # Check if the sum is correct
                results.append(path[:])  # make a copy
                return
            # If remaining < 0, no point in continuing
            if remaining < 0:
                return

            # Try all possible numbers from 'start' to 9
            for num in range(start, 9+1):
                # If num is bigger than remaining, no need to go further since numbers are increasing
                if num > remaining:
                    break

                path.append(num)
                # Move to the next number, and reduce the remaining sum
                backtrack(num + 1, remaining - num, path)
                path.pop()  # backtrack

        backtrack(1, n, [])
        return results


def main():
    k = 3
    n = 7
    print(Solution().combinationSum3(k, n))
    k = 3
    n = 9
    print(Solution().combinationSum3(k, n))


if __name__ == '__main__':
    main()
