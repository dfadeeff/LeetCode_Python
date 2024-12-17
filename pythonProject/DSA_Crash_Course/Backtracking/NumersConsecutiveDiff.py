from typing import List


class Solution:
    def numsSameConsecDiff(self, n: int, k: int) -> List[int]:
        results = []

        def backtrack(length_so_far, last_digit, path):
            """

            :param length_so_far: how many digits we’ve chosen so far.
            :param last_digit: the digit we placed in the previous step (to compute next valid digits).
            :param path: collection of digits chosen so far.
            :return:
            """
            # If we've built a number with n digits, record it
            if length_so_far == n:
                # Convert digits in path to integer
                num = int("".join(map(str, path)))
                results.append(num)
                return

            # Next digits to consider:
            # If k == 0, there's only one choice: next_digit = last_digit
            # If k > 0, there could be up to two choices: last_digit + k and last_digit - k

            # For convenience, put possible next digits in a set or list:
            next_candidates = set()
            if last_digit + k <= 9:
                next_candidates.add(last_digit + k)
            if last_digit - k >= 0:
                next_candidates.add(last_digit - k)

            for next_digit in next_candidates:
                path.append(next_digit)
                backtrack(length_so_far + 1, next_digit, path)
                path.pop()  # backtrack

        # Initialize by picking the first digit from 1 to 9
        for first_digit in range(1, 10):
            backtrack(1, first_digit, [first_digit])

        return results


def main():
    n = 3
    k = 7
    print(Solution().numsSameConsecDiff(n, k))
    n = 2
    k = 1
    print(Solution().numsSameConsecDiff(n, k))


if __name__ == '__main__':
    main()
