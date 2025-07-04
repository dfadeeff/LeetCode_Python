from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        window = set()
        left = 0

        for right in range(0, len(nums)):

            while abs(right - left) > k:
                window.remove(nums[left])
                left += 1
            if nums[right] in window:
                return True
            window.add(nums[right])
        return False


if __name__ == "__main__":
    nums = [1, 2, 3, 1]
    k = 3
    print(Solution().containsNearbyDuplicate(nums, k))
    nums = [1, 0, 1, 1]
    k = 1
    print(Solution().containsNearbyDuplicate(nums, k))
    nums = [1, 2, 3, 1, 2, 3]
    k = 2
    print(Solution().containsNearbyDuplicate(nums, k))
