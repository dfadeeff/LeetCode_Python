from typing import List


class Solution:
    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        asteroids.sort()
        for asteroid in asteroids:
            if asteroid > mass:
                return False
            mass += asteroid

        return True


def main():
    mass = 10
    asteroids = [3, 9, 19, 5, 21]
    print(Solution().asteroidsDestroyed(mass, asteroids))
    mass = 5
    asteroids = [4, 9, 23, 4]
    print(Solution().asteroidsDestroyed(mass, asteroids))


if __name__ == '__main__':
    main()
