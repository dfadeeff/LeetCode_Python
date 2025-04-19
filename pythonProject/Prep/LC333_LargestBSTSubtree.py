# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def largestBSTSubtree(self, root: Optional[TreeNode]) -> int:

        self.ans = 0
        def dfs(node):
            if not node:
                return float("inf"),float("-inf"),0

            lmin, lmax, lsize = dfs(node.left)
            rmin, rmax, rsize = dfs(node.right)

            # Check BST property: everything in left < node.val < everything in right
            if lmax < node.val < rmin:
                size = 1 + lsize + rsize
                # Update global answer
                self.ans = max(self.ans, size)
                # New subtree min is either left.min or node.val if left was empty
                # New subtree max is either right.max or node.val if right was empty
                return min(lmin, node.val), max(rmax, node.val), size
            else:
                # Not a BST here, return size=0 so parents won’t count it,
                # and give min/max values that will violate any parent check.
                return float('-inf'), float('inf'), 0

        dfs(root)
        return self.ans


if __name__ == "__main__":
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(8)
    root.right.right = TreeNode(7)
    print(Solution().largestBSTSubtree(root))
