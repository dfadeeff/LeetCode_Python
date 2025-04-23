from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:

    def closestValue(self, root: Optional[TreeNode], target: float) -> int:
        """binary search"""
        closest = root.val
        while root:
            closest = min(root.val, closest, key=lambda x: (abs(target - x), x))
            root = root.left if target < root.val else root.right
        return closest


if __name__ == "__main__":
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(5)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    target = 3.714286
    print(Solution().closestValue(root, target))
