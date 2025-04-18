from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """numbers are 1 indexed so add 1 to the index!"""
        l, r = 0, len(numbers) - 1
        while l < r:
            candidate = numbers[l] + numbers[r]
            if candidate > target:
                r -= 1
            elif candidate < target:
                l += 1
            else:
                return [l + 1, r + 1]
        return []


if __name__ == "__main__":
    numbers = [2, 7, 11, 15]
    target = 9
    print(Solution().twoSum(numbers, target))
    numbers = [2, 3, 4]
    target = 6
    print(Solution().twoSum(numbers, target))