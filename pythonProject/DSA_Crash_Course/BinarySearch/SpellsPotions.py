from typing import List


class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        def binary_search(arr, target):
            left = 0
            right = len(arr)
            while left < right:
                mid = (left + right) // 2
                if arr[mid] >= target:
                    right = mid
                else:
                    left = mid + 1

            return left

        potions.sort()
        ans = []
        m = len(potions)

        for spell in spells:
            i = binary_search(potions, success / spell)
            ans.append(m - i)

        return ans


def main():
    spells = [5, 1, 3]
    potions = [1, 2, 3, 4, 5]
    success = 7
    print(Solution().successfulPairs(spells, potions, success))

    spells = [3, 1, 2]
    potions = [8, 5, 8]
    success = 16
    print(Solution().successfulPairs(spells, potions, success))


if __name__ == '__main__':
    main()
