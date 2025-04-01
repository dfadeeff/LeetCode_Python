from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        return self.helper(0, len(nums) - 1)

    def helper(self, left, right) -> Optional[TreeNode]:
        if (left > right):
            return None
        pivot = (left + right) // 2

        # preorder traversal
        root = TreeNode(nums[pivot])
        root.left = self.helper(left, pivot - 1)
        root.right = self.helper(pivot + 1, right)
        return root


if __name__ == '__main__':
    nums = [-10, -3, 0, 5, 9]
    print(Solution().sortedArrayToBST(nums))
