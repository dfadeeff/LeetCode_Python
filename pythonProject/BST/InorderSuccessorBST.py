from typing import Optional


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def inorderSuccessor(self, root: TreeNode, p: TreeNode) -> Optional[TreeNode]:
        nodes = []

        def inorder_dfs(node):
            if not node:
                return

            inorder_dfs(node.left)
            nodes.append(node)
            inorder_dfs(node.right)

        inorder_dfs(root)  # Step 1: In-order traversal

        # Step 2: Find p in the list and return the next node
        for i in range(len(nodes) - 1):
            if nodes[i] == p:
                return nodes[i + 1]
        return None


if __name__ == '__main__':
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)
    p_node = root.left
    print(Solution().inorderSuccessor(root, p_node))
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.left.left.left = TreeNode(1)
    p_node = root.right
    print(Solution().inorderSuccessor(root, p_node))
