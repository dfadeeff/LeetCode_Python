# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0

        def dfs(node):
            nonlocal diameter
            if not node:
                return 0
            if not node.left and not node.right:
                return 1
            left = dfs(node.left)
            right = dfs(node.right)
            diameter = max(diameter, left + right)

            # move up in the tree
            return max(left, right) + 1

        dfs(root)
        return diameter


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    print(Solution().diameterOfBinaryTree(root))