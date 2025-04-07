from typing import List


class SparseVector:
    def __init__(self, nums: List[int]):
        """
        If nums1 = [1, 0, 0, 2, 3],
        → self.pairs = [[0, 1], [3, 2], [4, 3]]

        If nums2 = [0, 3, 0, 4, 0],
        → self.pairs = [[1, 3], [3, 4]]

        :param nums:
        """
        self.pairs = []
        for index, value in enumerate(nums):
            if value != 0:
                self.pairs.append([index, value])  # store as list of index-value pairs

    def dotProduct(self, vec: 'SparseVector') -> int:
        """
        p points to first element of self.pairs
        q points to first element of vec.pairs

        Time Complexity:
        (N + M), where:
	    •	N = len(self.pairs)
	    •	M = len(vec.pairs)

        Space Complexity:
	    O(N) for storing non-zero pairs.
        """
        result = 0
        p, q = 0, 0

        while p < len(self.pairs) and q < len(vec.pairs):
            index1, value1 = self.pairs[p]
            index2, value2 = vec.pairs[q]

            if index1 == index2:
                result += value1 * value2
                p += 1
                q += 1
            elif index1 < index2:
                p += 1
            else:
                q += 1

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
