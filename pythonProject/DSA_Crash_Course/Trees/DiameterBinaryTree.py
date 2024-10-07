from typing import Optional


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0

        def longest_path(node):
            if not node:
                return 0
            nonlocal diameter
            # recursively find the longest path in
            # both left child and right child
            left_path = longest_path(node.left)
            right_path = longest_path(node.right)

            # update the diameter if left_path plus right_path is larger
            diameter = max(diameter, left_path + right_path)

            # return the longest one between left_path and right_path;
            # remember to add 1 for the path connecting the node and its parent
            return max(left_path, right_path) + 1

        longest_path(root)
        return diameter


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    #
    #
    #

    node5 = TreeNode(55)
    node4 = TreeNode(4)
    node3 = TreeNode(3)
    node2 = TreeNode(2, left=node4, right=node5)
    root = TreeNode(1, left=node2, right=node3)
    solution = Solution()
    print(solution.diameterOfBinaryTree(root))


if __name__ == '__main__':
    main()
