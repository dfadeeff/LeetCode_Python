from typing import Optional


# Definition for a binary tree node.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def getPlaces(num: int):
            if not num:
                return 10

            places = 1
            while num > 0:
                num = num // 10
                places *= 10
            return places

        def dfs(node, current):
            if not node:
                return 0

            # shift the old prefix by the right power,
            # then append this node’s val
            current = current * getPlaces(node.val) + int(node.val)
            if not node.left and not node.right:
                return current
            left = dfs(node.left, current)
            right = dfs(node.right, current)
            return left + right

        return dfs(root, 0)


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(79, right=TreeNode(111))
    root.right = TreeNode(2)
    print(Solution().sumNumbers(root))
