from typing import Optional


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        def helper(node, cur_max, cur_min):
            # if encounter leaves, return the max-min along the path
            if not node:
                return cur_max - cur_min
            # else, update max and min
            # and return the max of left and right subtrees
            cur_max = max(cur_max, node.val)
            cur_min = min(cur_min, node.val)
            left = helper(node.left, cur_max, cur_min)
            right = helper(node.right, cur_max, cur_min)
            return max(left, right)

        return helper(root, root.val, root.val)





def main():
    # Create the binary tree from the example
    # Tree structure:
    #       1
    #        \
    #         2
    #          \
    #           0
    #          /
    #         3
    #
    # case1
    node15 = TreeNode(15)
    node7 = TreeNode(6)
    node20 = TreeNode(20, left=node15, right=node7)
    node9 = TreeNode(9)
    root1 = TreeNode(3, left=node9, right=node20)
    solution = Solution()
    print(solution.maxAncestorDiff(root1))

if __name__ == '__main__':
    main()
