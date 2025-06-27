from typing import List


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pair = [[p, s] for p, s in zip(position, speed)]

        stack = []
        for p,s in sorted(pair)[::-1]:
            stack.append((target-p) / s)
            if len(stack) > 1 and stack[-1] <= stack[-2]:
                stack.pop()
            return len(stack)




if __name__ == "__main__":
    target = 12
    position = [10, 8, 0, 5, 3]
    speed = [2, 4, 1, 1, 3]
    print(Solution().carFleet(target, position, speed))
