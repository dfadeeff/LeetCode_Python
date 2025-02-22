from typing import Optional

from TreeNode import TreeNode


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        def dfs(root, curr):
            if not root:
                return False

            if root.left is None or root.right is None:
                return (curr + root.val) == targetSum

            curr += root.val
            left = dfs(root.left, curr)
            right = dfs(root.right, curr)
            return left or right

        return dfs(root, float("-inf"))


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    print(Solution().hasPathSum(root, 5))
