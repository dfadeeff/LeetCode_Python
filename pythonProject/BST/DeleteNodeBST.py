from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None  # Base case: key not found

        # Step 1: Find the node to delete
        if key < root.val:
            root.left = self.deleteNode(root.left, key)  # Search left subtree
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)  # Search right subtree
        else:
            # Node found, handle deletion cases

            # Case 1: Node is a leaf or has only one child
            if not root.left:
                return root.right  # Replace node with its right child (or None)
            if not root.right:
                return root.left  # Replace node with its left child

            # Case 2: Node has two children
            # Find in-order successor (smallest node in right subtree)
            successor = self.getMin(root.right)

            # Copy the successor's value to the node
            root.val = successor.val

            # Delete the successor (since it's now duplicated)
            root.right = self.deleteNode(root.right, successor.val)

        return root

    def getMin(self, node: TreeNode) -> TreeNode:
        """Finds the leftmost (smallest) node in a subtree."""
        while node.left:
            node = node.left
        return node


if __name__ == '__main__':
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(7)
    print(Solution().deleteNode(root, 3))
