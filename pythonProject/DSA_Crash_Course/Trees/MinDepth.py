from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(root):
            if root is None:
                return 0
            # If only one of child is non-null, then go into that recursion.
            if not root.left :
                return 1 + dfs(root.right)
            elif not root.right:
                return 1 + dfs(root.left)
            # Both children are non-null, hence call for both children.
            return 1 + min(dfs(root.left), dfs(root.right))

        return dfs(root)


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       3
    #      / \
    #     9   20
    #        / \
    #       15  7
    #
    #
    #
    # case1
    node15 = TreeNode(15)
    node7 = TreeNode(6)
    node20 = TreeNode(20, left=node15, right=node7)
    node9 = TreeNode(9)
    root1 = TreeNode(3, left=node9, right=node20)

    # Calculate the max depth
    solution1 = Solution()
    # max_depth = solution.maxDepth(root)
    min_depth1 = solution1.minDepth(root1)
    print(f"The minimum depth of the tree is: {min_depth1}")

    # case 2
    node6 = TreeNode(6)
    node5 = TreeNode(5, right=node6)
    node4 = TreeNode(4, right=node5)
    node3 = TreeNode(3, right=node4)
    root2 = TreeNode(2, right=node3)
    solution2 = Solution()
    min_depth2 = solution2.minDepth(root2)
    print(f"The minimum depth of the tree is: {min_depth2}")


if __name__ == "__main__":
    main()
