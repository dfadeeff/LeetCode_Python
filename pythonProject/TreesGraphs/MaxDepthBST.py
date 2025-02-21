from typing import Optional

from TreeNode import TreeNode


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)
        return max(left, right) + 1

    def maxDepthIterative(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        stack = [(root, 1)]
        ans = 0
        while stack:
            node, depth = stack.pop()
            ans = max(ans, depth)
            # if node is not empty, ie left child not empty
            if node.left:
                stack.append((node.left, depth + 1))
            # if node is not empty, ie right child not empty
            if node.right:
                stack.append((node.right, depth + 1))
        return ans


if __name__ == '__main__':
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.left.left = TreeNode(15)
    root.left.right = TreeNode(7)
    print(Solution().maxDepth(root))
    print(Solution().maxDepthIterative(root))
