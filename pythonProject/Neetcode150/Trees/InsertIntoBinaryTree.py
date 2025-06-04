from typing import Optional


# Definition for a binary tree node.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return TreeNode(val)
        if val > root.val:
            root.right = self.insertIntoBST(root.right, val)
        else:
            root.left = self.insertIntoBST(root.left, val)
        return root


def print_inorder(root):
    if not root:
        return
    print_inorder(root.left)
    print(root.val, end=" ")
    print_inorder(root.right)


if __name__ == "__main__":
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(7)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    new_tree = Solution().insertIntoBST(root, 5)
    print_inorder(new_tree)  # Output: 1 2 3 4 5 7
