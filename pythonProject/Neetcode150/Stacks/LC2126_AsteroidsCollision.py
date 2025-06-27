from typing import List

class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        for i in asteroids:
            while stack and i <0 and stack[-1] > 0:
                diff = i + stack[-1]
                if diff < 0:
                    stack.pop()
                elif diff > 0:
                    i = 0
                else: #destroy both of the asteroids
                    i = 0
                    stack.pop()
            if i:
                stack.append(i)
        return stack



if __name__ == "__main__":
    asteroids = [5, 10, -5]
    print(Solution().asteroidCollision(asteroids))
    asteroids = [8, -8]
    print(Solution().asteroidCollision(asteroids))
    asteroids = [10, 2, -5]
    print(Solution().asteroidCollision(asteroids))