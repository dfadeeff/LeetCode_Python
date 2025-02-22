from typing import Optional

from TreeNode import TreeNode


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        def dfs(node, curr):
            """BASE CASES : if node is None, no path, return False"""
            if not node:
                return False
            # If at a leaf, ie if both children are null, then the node is a leaf
            if node.left is None and node.right is None:
                return (curr + node.val) == targetSum

            curr += node.val
            left = dfs(node.left, curr)
            right = dfs(node.right, curr)
            return left or right

        return dfs(root, 0)

    def hasPathSumIterative(self, root: Optional[TreeNode], targetSum: int) -> bool:

        if not root:
            return False

        stack = [(root, 0)]
        while stack:
            node, curr = stack.pop()
            # if both children are null, then the node is a leaf
            if node.left == None and node.right == None:
                if (curr + node.val) == targetSum:
                    return True

            curr += node.val
            if node.left:
                stack.append((node.left, curr))
            if node.right:
                stack.append((node.right, curr))

        return False


if __name__ == "__main__":
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.left.left = TreeNode(11)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right = TreeNode(8)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.right.right.right = TreeNode(1)
    print(Solution().hasPathSum(root, 22))
    print(Solution().hasPathSumIterative(root, 22))
