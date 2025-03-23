from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def dfs(node):
            if node is None:
                return (True, 0)
            left_balanced, left_height = dfs(node.left)
            right_balanced, right_height = dfs(node.right)
            if not left_balanced or not right_balanced:
                return (False, 0)
            # Check current node
            if abs(left_height - right_height) > 1:
                return (False, 0)

            return (True, max(left_height, right_height) + 1)
        balanced, height = dfs(root)
        return balanced


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().isBalanced(root))
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(3)
    root.left.left.left = TreeNode(4)
    root.left.left.right = TreeNode(4)
    print(Solution().isBalanced(root))
