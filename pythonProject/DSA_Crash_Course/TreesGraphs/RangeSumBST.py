from typing import Optional
from xml.dom.expatbuilder import TEXT_NODE

from pygments import highlight


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rangeSumBSTSlow(self, root: Optional[TreeNode], low: int, high: int) -> int:
        ans = 0

        if low <= root.val <= high:
            ans += root.val
        # Recursion on left and right subtree
        ans += self.rangeSumBSTSlow(root.left, low, high)
        ans += self.rangeSumBSTSlow(root.right, low, high)

        return ans

    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if not root:
            return 0

        ans = 0

        if low <= root.val <= high:
            ans += root.val

        if low < root.val:
            ans += self.rangeSumBST(root.left, low, high)
        if root.val < high:
            ans += self.rangeSumBST(root.right, low, high)

        return ans


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       10
    #      / \
    #     5   15
    #    / \    \
    #    3  7    18
    #
    #
    #

    node18Leaf = TreeNode(18)
    node3Leaf = TreeNode(3)
    node7Leaf = TreeNode(7)
    node5 = TreeNode(5, left=node3Leaf, right=node7Leaf)
    node15 = TreeNode(15, right=node18Leaf)

    root = TreeNode(10, left=node5, right=node15)
    solution = Solution()
    print(solution.rangeSumBST(root, low=7, high=15))


if __name__ == '__main__':
    main()
