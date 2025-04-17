from typing import List


class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        count = 0
        for i in range(len(flowerbed)):
            if flowerbed[i] == 0:
                # check left and right empty
                left = (i==0) or flowerbed[i-1] == 0
                right = (i==len(flowerbed)-1) or flowerbed[i+1] == 0
                if left and right:
                    flowerbed[i] = 1
                    count += 1
        return count >= n


if __name__ == "__main__":
    flowerbed = [1, 0, 0, 0, 1]
    n = 1
    print(Solution().canPlaceFlowers(flowerbed, n))
    flowerbed = [1, 0, 0, 0, 1]
    n = 2
    print(Solution().canPlaceFlowers(flowerbed, n))
