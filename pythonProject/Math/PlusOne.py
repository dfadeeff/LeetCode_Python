from typing import List

from pygments.lexers import graph


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        digit = 0
        for i in range(len(digits)):
            power = len(digits) - 1 - i
            digit += digits[i] * 10 ** power
        plus_one = digit + 1

        # one option
        ans = [int(x) for x in str(plus_one)]
        return ans


if __name__ == '__main__':
    digits = [1, 2, 3]
    print(Solution().plusOne(digits))
    digits = [4, 3, 2, 1]
    print(Solution().plusOne(digits))
    digits = [9]
    print(Solution().plusOne(digits))
