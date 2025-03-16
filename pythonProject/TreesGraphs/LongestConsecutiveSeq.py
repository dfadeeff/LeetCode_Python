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

        def dfs(node, parent_val, length):
            nonlocal max_length
            if not node:
                return

            if node.val == parent_val + 1:
                length += 1
            else:
                length = 1  # Reset sequence length

            # Update max_length globally
            max_length = max(max_length, length)

            # Continue exploring children
            dfs(node.left, node.val, length)
            dfs(node.right, node.val, length)

        dfs(root, root.val - 1, 0)

        return max_length


if __name__ == '__main__':
    root = TreeNode(1)
    root.right = TreeNode(3)
    root.right.left = TreeNode(2)
    root.right.right = TreeNode(4)
    root.right.right.right = TreeNode(5)
    print(Solution().longestConsecutive(root))
