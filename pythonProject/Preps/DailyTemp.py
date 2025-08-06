from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        answer = [0] * len(temperatures)
        for i in range(len(temperatures)):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                prev_index = stack.pop()
                answer[prev_index] = i - prev_index

            stack.append(i)
        return answer


if __name__ == "__main__":
    temperatures = [34, 33, 32, 31, 30, 50]
    print(Solution().dailyTemperatures(temperatures))
