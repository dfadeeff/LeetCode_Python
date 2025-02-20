class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


if __name__ == "__main__":
    """
         1
        / \
        2  3
        /\
        4  5
    """

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)


    # Function to print tree in-order
    def inorder_traversal(node):
        if node is not None:
            inorder_traversal(node.left)
            print(node.val, end=" ")
            inorder_traversal(node.right)


    print(inorder_traversal(root))
