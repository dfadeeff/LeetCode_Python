# Definition for a binary tree node.
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        if not postorder or not inorder:
            return None

        root_val = postorder[-1]

        root = TreeNode(root_val)

        # find root in inorder, to split into left/right subtree
        mid = inorder.index(root_val)

        # recursive construction
        root.left = self.buildTree(inorder[0: mid], postorder[:mid], )
        root.right = self.buildTree(inorder[mid + 1:], postorder[mid:-1], )

        return root


if __name__ == '__main__':
    inorder = [9, 3, 15, 20, 7]
    postorder = [9, 15, 7, 20, 3]
    print(Solution().buildTree(inorder, postorder))
