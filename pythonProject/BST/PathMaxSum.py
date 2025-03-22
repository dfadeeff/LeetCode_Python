from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        max_sum = float('-inf')

        def dfs(node):
            nonlocal max_sum
            if not node:
                return 0
            left_sum = max(dfs(node.left), 0)
            right_sum = max(dfs(node.right), 0)

            # max path going through this path
            current_path = node.val + left_sum + right_sum
            max_sum = max(max_sum, current_path)

            # return to parent, only one side
            return node.val + max(left_sum, right_sum)

        dfs(root)
        return max_sum


if __name__ == '__main__':
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().maxPathSum(root))
