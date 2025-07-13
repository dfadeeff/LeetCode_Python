from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        maxLeft = [0] * n
        maxRight = [0] * n

        maxLeft[0] = 0
        for i in range(1, n):
            maxElem = max(height[i - 1], maxLeft[i - 1])
            maxLeft[i] = maxElem

        maxRight[n - 1] = 0
        for i in range(n - 2, -1, -1):
            maxElem = max(height[i + 1], maxRight[i + 1])
            maxRight[i] = maxElem

        minLR = [0] * n
        for i in range(len(minLR)):
            minLR[i] = min(maxLeft[i], maxRight[i])

        ans = 0
        for i in range(len(height)):
            maxElem = max(minLR[i] - height[i],0)
            ans += maxElem
        return ans


if __name__ == "__main__":
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(Solution().trap(height))
