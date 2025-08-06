from typing import List

from pygments.lexers.soong import SoongLexer


class Solution:
    def finalPrices(self, prices: List[int]) -> List[int]:
        stack = []

        for i in range(len(prices)):
            while stack and prices[stack[-1]] >= prices[i]:
                prev_index = stack.pop()

                prices[prev_index] -= prices[i]
            stack.append(i)

        return prices


if __name__ == "__main__":
    prices = [8, 4, 6, 2, 3]
    print(Solution().finalPrices(prices))
