from typing import Optional


# Definition for a binary tree node.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def dfs(node, current, num_neg):
            if not node:
                return 0
            current = current * 10 + abs(node.val)
            if node.val < 0:
                num_neg += 1

            if not node.left and not node.right:
                sign = -1 if num_neg % 2 == 1 else 1
                return current * sign
            left = dfs(node.left, current, num_neg)
            right = dfs(node.right, current, num_neg)
            return left + right

        return dfs(root, 0, 0)


if __name__ == "__main__":
    root = TreeNode(1,
                    left=TreeNode(-2),
                    right=TreeNode(3))
    print(Solution().sumNumbers(root))  # 1
