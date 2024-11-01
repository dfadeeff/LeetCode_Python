from typing import List


class Solution:
    def maxNumberOfApples(self, weight: List[int]) -> int:
        sorted_weights = sorted(weight, reverse=False)
        print(sorted_weights)

        ans = 0
        sum = 0
        for i in range(len(sorted_weights)):

            sum += sorted_weights[i]
            if sum > 5000:
                break
            ans += 1

        return ans


def main():
    weight = [100, 200, 150, 1000]
    print(Solution().maxNumberOfApples(weight))
    weight = [900, 950, 800, 1000, 700, 800]
    print(Solution().maxNumberOfApples(weight))


if __name__ == '__main__':
    main()
