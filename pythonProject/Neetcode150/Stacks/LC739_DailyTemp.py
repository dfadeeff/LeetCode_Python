from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        # monotonic decreasing order
        res = [0] * len(temperatures)
        stack = []  # pair [temp, index]
        for i, t in enumerate(temperatures):
            while stack and t > stack[-1][0]:  # first element is temperature in the pair
                stackTemp, stackIndex = stack.pop()
                res[stackIndex] = (i - stackIndex)

            stack.append([t, i])

        return res


if __name__ == "__main__":
    temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
    print(Solution().dailyTemperatures(temperatures))
