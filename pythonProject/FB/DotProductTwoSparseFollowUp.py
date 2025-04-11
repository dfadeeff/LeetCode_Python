from typing import List


class SparseVector:
    """
    Follow up if vectors are drastically different
    """

    def __init__(self, nums: List[int]):
        self.nums = []
        for i, num in enumerate(nums):
            if num:
                self.nums.append((i, num))

    def dotProduct(self, vec: 'SparseVector') -> int:
        dot_product = 0
        if len(self.nums) < len(vec.nums):
            for idx, num in self.nums:
                dot_product += num * self.binary_search(vec.nums, idx)
        else:
            for idx, num in vec.nums:
                dot_product += num * self.binary_search(self.nums, idx)

        return dot_product

    def binary_search(self, nums: List[int], i: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid][0] == i:
                return nums[mid][1]
            elif nums[mid][0] < i:
                left = mid + 1
            else:
                right = mid - 1
        return 0


if __name__ == '__main__':
    nums1 = [1, 0, 0, 2, 3]
    nums2 = [0, 3, 0, 4, 0]
    print(SparseVector(nums1).dotProduct(SparseVector(nums2)))
