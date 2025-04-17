# Definition for a binary tree node.
from collections import deque
from typing import Optional, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        to_delete = set(to_delete) # O(1)

        self.forest = []
        self.dfs(root, to_delete,True)
        return self.forest

    def dfs(self, node, to_delete, is_root):
        if not node:
            return
        if node.val in to_delete:
            self.dfs(node.left, to_delete, True)
            self.dfs(node.right, to_delete, True)
        else:
            if node.left:
                if node.left.val in to_delete:
                    self.dfs(node.left, to_delete, True)
                    node.left = None
                else:
                    self.dfs(node.left, to_delete,False)
            if node.right:
                if node.right.val in to_delete:
                    self.dfs(node.right, to_delete, True)
                    node.right = None
                else:
                    self.dfs(node.right, to_delete, False)

            if is_root:
                self.forest.append(node)



if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    to_delete = [3, 5]
    print(Solution().delNodes(root, to_delete))
