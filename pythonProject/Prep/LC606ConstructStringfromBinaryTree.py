# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


from typing import Optional


class Solution:
    def tree2str(self, root: Optional[TreeNode]) -> str:
        # res = []
        #
        # def dfs(node):
        #     if not node:
        #         return
        #     res.append(node.val)
        #     dfs(node.left)
        #     dfs(node.right)
        #
        # dfs(root)
        # return res

        # Start with the root value
        s = str(root.val)
        # If there's a left child or a right child, we need to include parentheses for the left
        if root.left:
            s += f"({self.tree2str(root.left)})"
        elif root.right:
            s += "()"
        if root.right:
            s += f"({self.tree2str(root.right)})"
        return s


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(4)
    root.right = TreeNode(3)
    print(Solution().tree2str(root))
