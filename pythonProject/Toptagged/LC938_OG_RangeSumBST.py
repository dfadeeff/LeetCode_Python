from typing import Optional

from sqlalchemy.log import rootlogger


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if not root:
            return 0
        ans = 0
        stack = [root]
        while stack:
            node = stack.pop()
            if node:
                # 1) If node is in range, add its value
                if low <= node.val <= high:
                    ans += node.val
                # 2) If there might be values ≥ low in the left subtree, explore it
                if low < node.val:
                    stack.append(node.left)

                # 3) If there might be values ≤ high in the right subtree, explore it
                if node.val < high:
                    stack.append(node.right)
        return ans


if __name__ == "__main__":
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(7)
    root.right = TreeNode(15)
    root.right.right = TreeNode(18)
    low = 7
    high = 15
    print(Solution().rangeSumBST(root, low, high))
