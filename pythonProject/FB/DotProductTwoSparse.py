from typing import List


class SparseVector:
    def __init__(self, nums: List[int]):
        self.nums = []

        for i, num in enumerate(nums):
            if num:
                self.nums.append((i, num))

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec: 'SparseVector') -> int:
        # each vector contains tuples

        dot_product = 0
        i, j = 0, 0
        while i < len(self.nums) and j < len(vec.nums):
            i_idx, i_num = self.nums[i]
            j_idx, j_num = vec.nums[j]

            if i_idx == j_idx:
                dot_product += i_num * j_num
                i += 1
                j += 1
            elif i_idx < j_idx:
                i += 1
            else:
                j += 1

        return dot_product


if __name__ == '__main__':
    nums1 = [1, 0, 0, 2, 3]
    nums2 = [0, 3, 0, 4, 0]
    print(SparseVector(nums1).dotProduct(SparseVector(nums2)))
