# Definition for a binary tree node.
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        list_of_nodes = []
        def dfs(node):
            if not node:
                return

            dfs(node.left)
            list_of_nodes.append(node.val)
            dfs(node.right)
        dfs(root)
        return list_of_nodes





if __name__ == '__main__':
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.left = TreeNode(3)
    print(Solution().inorderTraversal(root))
