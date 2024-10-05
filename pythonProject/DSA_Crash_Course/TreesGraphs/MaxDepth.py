from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        stack = [(root, 1)]
        ans = 0
        while stack:
            node, depth = stack.pop()
            ans = max(ans, depth)
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        return ans


    def maxDepthRecursive(self, root: Optional[TreeNode]) -> int:
        # base case
        if not root:
            return 0

        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)
        return max(left, right) + 1


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    #  /
    # 6

    node6 = TreeNode(6)
    node4 = TreeNode(4, left=node6)
    node5 = TreeNode(5)
    node2 = TreeNode(2, left=node4, right=node5)
    node3 = TreeNode(3)
    root = TreeNode(1, left=node2, right=node3)

    # Calculate the max depth
    solution = Solution()
    #max_depth = solution.maxDepth(root)
    max_depth = solution.maxDepthRecursive(root)
    print(f"The maximum depth of the tree is: {max_depth}")


if __name__ == "__main__":
    main()