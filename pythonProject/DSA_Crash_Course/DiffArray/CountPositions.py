from typing import List


class Solution:
    def meetRequirement(self, n: int, lights: List[List[int]], requirement: List[int]) -> int:
        diff = [0 for _ in range(n + 1)]
        for position, radius in lights:
            diff[max(0, position - radius)] += 1
            diff[min(n - 1, position + radius) + 1] -= 1

        for i in range(1, len(diff)):
            diff[i] += diff[i - 1]
        # print("final diff:", diff)

        ans = 0
        for i in range(0, n):
            if diff[i] >= requirement[i]:
                ans += 1

        # print(diff)

        return ans

    # def meetRequirementTLE(self, n: int, lights: List[List[int]], requirement: List[int]) -> int:
    #     arr = [0] * (n)
    #     for position, radius in lights:
    #         left = position - radius
    #         right = position + radius
    #         for i in range(max(0, left), min(n - 1, right) + 1):
    #             arr[i] += 1
    #
    #     ans = 0
    #     for i in range(n):
    #         if arr[i] >= requirement[i]:
    #             ans += 1
    #     return ans


def main():
    n = 5
    lights = [[0, 1], [2, 1], [3, 2]]
    requirement = [0, 2, 1, 4, 1]
    print(Solution().meetRequirement(n, lights, requirement))
    n = 1
    lights = [[0, 1]]
    requirement = [2]
    print(Solution().meetRequirement(n, lights, requirement))


if __name__ == '__main__':
    main()
