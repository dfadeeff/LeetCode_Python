from typing import Optional

from sqlalchemy.log import rootlogger


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if not root:
            return 0
        if root.val < low:
            return self.rangeSumBST(root.right, low, high)
        if root.val > high:
            return self.rangeSumBST(root.left, low, high)
        return self.rangeSumBST(root.left, low, high) + self.rangeSumBST(root.right, low, high) + root.val


if __name__ == "__main__":
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(7)
    root.right = TreeNode(15)
    root.right.right = TreeNode(18)
    low = 7
    high = 15
    print(Solution().rangeSumBST(root, low, high))
