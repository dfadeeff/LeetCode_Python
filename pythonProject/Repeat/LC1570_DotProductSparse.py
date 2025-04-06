from typing import List

from pythonProject.DSA_Crash_Course.BinarySearch.DivideChocolate import Solution


class SparseVector:
    def __init__(self, nums: List[int]):
        """use index, value pairs"""
        # Only store non-zero entries in a dictionary
        self.non_zero = {i: num for i, num in enumerate(nums) if num != 0}

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec: 'SparseVector') -> int:
        if len(self.non_zero) > len(vec.non_zero):
            return vec.dotProduct(self)  # Swap to minimize iterations
        result = 0
        for i, val in self.non_zero.items():
            if i in vec.non_zero:
                result += val * vec.non_zero[i]
        return result


if __name__ == "__main__":
    nums1 = [1, 0, 0, 2, 3]
    nums2 = [0, 3, 0, 4, 0]
    print("nums1: ", nums1)
    print("nums2: ", nums2)
    v1 = SparseVector(nums1)
    v2 = SparseVector(nums2)
    ans = v1.dotProduct(v2)
    print("ans: ", ans)
