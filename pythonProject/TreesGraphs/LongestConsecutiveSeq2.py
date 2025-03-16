# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def longestConsecutive(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        max_length = 0

        def dfs(node):
            """The helper function dfs recursively calculates, at every node, the longest increasing and decreasing sequences that start from that node going downward."""
            nonlocal max_length
            if not node:
                return (0, 0)  # (increasing_length, decreasing_length)

            inc, dec = 1, 1  # Start lengths at 1 (the node itself)

            # Explore left child
            if node.left:
                left_inc, left_dec = dfs(node.left)
                if node.val - node.left.val == 1:
                    dec = left_dec + 1
                elif node.val - node.left.val == -1:
                    inc = left_inc + 1

            # Explore right child
            if node.right:
                right_inc, right_dec = dfs(node.right)
                if node.val - node.right.val == 1:
                    dec = max(dec, right_dec + 1)
                elif node.val - node.right.val == -1:
                    inc = max(inc, right_inc + 1)

            # Combine increasing and decreasing through the current node
            # minus 1 to avoid counting current node twice
            max_length = max(max_length, inc + dec - 1)

            # Return lengths of the longest increasing and decreasing sequences downwards
            return (inc, dec)

        dfs(root)
        return max_length


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    print(Solution().longestConsecutive(root))
