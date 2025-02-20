# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
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


def build_tree_from_list(lst):
    if not lst:
        return None

    nodes = [TreeNode(val) if val is not None else None for val in lst]

    for i, node in enumerate(nodes):
        if node is not None:
            left_index = 2 * i + 1
            right_index = 2 * i + 2

            if left_index < len(nodes):
                node.left = nodes[left_index]
            if right_index < len(nodes):
                node.right = nodes[right_index]

    return nodes[0]

def test_isValidBST():
    root = build_tree_from_list([2, 1, 3])
    solution = Solution()
    assert solution.isValidBST(root) == True, "Test case failed!"
    print("Test case passed!")


if __name__ == '__main__':
    test_isValidBST()
