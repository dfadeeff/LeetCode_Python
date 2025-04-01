from typing import List


class Solution:
    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        asteroids.sort()
        #print(asteroids)
        for i in range(len(asteroids)):
            if mass >= asteroids[i]:
                mass += asteroids[i]
            else:
                return False
        return True




if __name__ == '__main__':
    mass = 10
    asteroids = [3, 9, 19, 5, 21]
    print(Solution().asteroidsDestroyed(mass, asteroids))
    mass = 5
    asteroids = [4, 9, 23, 4]
    print(Solution().asteroidsDestroyed(mass, asteroids))