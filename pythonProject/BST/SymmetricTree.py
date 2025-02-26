# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSymmetricWrong(self, root: Optional[TreeNode]) -> bool:
        list_of_nodes = []

        def dfs(node):
            if not node:
                return

            dfs(node.left)
            list_of_nodes.append(node.val)
            dfs(node.right)

        dfs(root)

        left = 0
        right = len(list_of_nodes) - 1
        while left <= right:
            if list_of_nodes[left] == list_of_nodes[right]:
                left += 1
                right -= 1
            else:
                return False

        return True

    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True  # An empty tree is symmetric

        return self.isMirror(root.left, root.right)  # Compare left & right subtrees

    def isMirror(self, left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
        if not left and not right:
            return True  # Both nodes are None (leaf nodes)
        if not left or not right:
            return False  # One node is None, the other isn't

        # Check if values are equal & mirror left.left with right.right, and left.right with right.left
        return (left.val == right.val and
                self.isMirror(left.left, right.right) and
                self.isMirror(left.right, right.left))


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.right = TreeNode(2)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(3)
    print(Solution().isSymmetric(root))
    print(Solution().isSymmetricWrong(root))
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.right = TreeNode(3)
    root.right = TreeNode(2)
    root.right.right = TreeNode(3)
    print(Solution().isSymmetric(root))
    print(Solution().isSymmetricWrong(root))
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(2)
    root.right = TreeNode(2)
    root.right.left = TreeNode(2)
    print(Solution().isSymmetric(root))
    print(Solution().isSymmetricWrong(root))
