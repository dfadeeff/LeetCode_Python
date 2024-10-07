from typing import Optional


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def dfs(node, small, large):
            if not node:
                return True

            if not (small < node.val < large):
                return False

            left = dfs(node.left, small, node.val)
            right = dfs(node.right, node.val, large)

            # tree is a BST if left and right subtrees are also BSTs
            return left and right

        return dfs(root, float("-inf"), float("inf"))
        return True

    def isValidBSTIterative(self, root: Optional[TreeNode]) -> bool:
        stack = [(root, float("-inf"), float("inf"))]
        while stack:
            node, small, large = stack.pop()
            if not (small < node.val < large):
                return False

            if node.left:
                stack.append((node.left, small, node.val))
            if node.right:
                stack.append((node.right, node.val, large))

        return True


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       4
    #      / \
    #     2   6
    #    / \
    #    1  3
    #
    #
    #

    node1Leaf = TreeNode(1)
    node3Leaf = TreeNode(3)
    node6Leaf = TreeNode(6)
    node2 = TreeNode(2, left=node1Leaf, right=node3Leaf)

    root = TreeNode(4, left=node2, right=node6Leaf)
    solution = Solution()
    print(solution.isValidBST(root))


if __name__ == '__main__':
    main()
