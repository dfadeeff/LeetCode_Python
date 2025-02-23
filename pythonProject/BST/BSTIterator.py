from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BSTIterator:
    def __init__(self, root: Optional[TreeNode]):
        self.stack = []
        self._leftmost_inorder(root)

    def _leftmost_inorder(self, node):
        """Helper function to push all left children of `node` onto the stack."""
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """Returns the next smallest number in in-order traversal."""
        top_node = self.stack.pop()  # Pop the smallest available node

        if top_node.right:
            self._leftmost_inorder(top_node.right)  # Process right subtree

        return top_node.val

    def hasNext(self) -> bool:
        """Returns True if there are more elements in in-order traversal."""
        return len(self.stack) > 0



if __name__ == '__main__':
    # Example Usage:
    # Tree structure:
    #       7
    #      / \
    #     3   15
    #        /  \
    #       9   20
    root = TreeNode(7)
    root.left = TreeNode(3)
    root.right = TreeNode(15)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(20)

    iterator = BSTIterator(root)
    print(iterator.next())  # Output: 3
    print(iterator.next())  # Output: 7
    print(iterator.hasNext())  # Output: True
    print(iterator.next())  # Output: 9
    print(iterator.hasNext())  # Output: True
    print(iterator.next())  # Output: 15
    print(iterator.hasNext())  # Output: True
    print(iterator.next())  # Output: 20
    print(iterator.hasNext())  # Output: False
