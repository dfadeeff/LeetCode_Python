from typing import List


class SparseVector:
    def __init__(self, nums: List[int]):
        # Store index ➝ value only for non-zero entries
        self.values = {i: num for i, num in enumerate(nums) if num != 0}

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec: 'SparseVector') -> int:
        # Only iterate over keys that exist in both vectors
        result = 0

        # Always iterate over smaller dict for efficiency
        if len(self.values) > len(vec.values):
            return vec.dotProduct(self)

        for i in self.values:
            if i in vec.values:
                result += self.values[i] * vec.values[i]
        return result


# Your SparseVector object will be instantiated and called as such:
# v1 = SparseVector(nums1)
# v2 = SparseVector(nums2)
# ans = v1.dotProduct(v2)

if __name__ == "__main__":
    nums1 = [1, 0, 0, 2, 3]
    nums2 = [0, 3, 0, 4, 0]
    v1 = SparseVector(nums1)
    v2 = SparseVector(nums2)
    ans = v1.dotProduct(v2)
    print(ans)
    nums1 = [0, 1, 0, 0, 0]
    nums2 = [0, 0, 0, 0, 2]
    v1 = SparseVector(nums1)
    v2 = SparseVector(nums2)
    ans = v1.dotProduct(v2)
    print(ans)
