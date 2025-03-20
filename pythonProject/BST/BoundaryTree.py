from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def boundaryOfBinaryTree(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        boundary = []

        def isLeaf(node):
            return node and not node.left and not node.right

        # 1. Add left boundary (excluding leaf)
        def addLeftBoundary(node):
            while node:
                if not isLeaf(node):
                    boundary.append(node.val)
                node = node.left if node.left else node.right

        # 2. Add leaves (DFS traversal)
        def addLeaves(node):
            if not node:
                return
            if isLeaf(node):
                boundary.append(node.val)
                return
            addLeaves(node.left)
            addLeaves(node.right)

        # 3. Add right boundary (excluding leaf), collected in stack to reverse
        def addRightBoundary(node):
            stack = []
            while node:
                if not isLeaf(node):
                    stack.append(node.val)
                node = node.right if node.right else node.left
            while stack:
                boundary.append(stack.pop())

        # Root is added if it's not a leaf
        if not isLeaf(root):
            boundary.append(root.val)

        addLeftBoundary(root.left)
        addLeaves(root)
        addRightBoundary(root.right)

        return boundary


if __name__ == "__main__":
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.left = TreeNode(3)
    root.right.right = TreeNode(4)
    print(Solution().boundaryOfBinaryTree(root))
