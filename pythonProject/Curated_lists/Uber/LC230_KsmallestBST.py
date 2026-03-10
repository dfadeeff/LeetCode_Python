from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        values = []

        def dfs(node):
            if not node:
                return

            dfs(node.left)
            values.append(node.val)
            dfs(node.right)

        dfs(root)

        return values[k-1]


if __name__ == "__main__":
    kThsmallest = Solution()
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.left.right = TreeNode(2)
    root.right = TreeNode(4)
    print(kThsmallest.kthSmallest(root, 1))
