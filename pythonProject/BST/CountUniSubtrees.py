from collections import deque
from typing import Optional

from pygments.lexer import default


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        self.count = 0  # Store total unival subtree count

        def dfs(node):
            if not node:
                return True  # Null nodes are considered unival

            # Recursively check left and right subtrees
            left_unival = dfs(node.left)
            right_unival = dfs(node.right)

            # Check if current node is unival
            if left_unival and right_unival:
                if node.left and node.left.val != node.val:
                    return False  # Left child has a different value
                if node.right and node.right.val != node.val:
                    return False  # Right child has a different value

                self.count += 1  # Increment unival subtree count
                return True  # This subtree is unival

            return False  # Not a unival subtree

        dfs(root)  # Start DFS traversal
        return self.count


if __name__ == '__main__':
    root = TreeNode(5)
    root.left = TreeNode(1)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(5)
    root.right = TreeNode(5)
    root.right.right = TreeNode(5)
    print(Solution().countUnivalSubtrees(root))
    root = TreeNode(5)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    print(Solution().countUnivalSubtrees(root))
