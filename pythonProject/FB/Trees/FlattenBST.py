from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if not root:
            return  # Edge case: Empty tree

        # Step 1: Store nodes in pre-order traversal
        node_list = []

        def dfs(root):
            if root is None:
                return
            node_list.append(root)  ## Collect nodes in pre-order
            dfs(root.left)
            dfs(root.right)

        dfs(root)  # Perform pre-order DFS and store nodes
        # Step 2: Modify the tree in-place
        for i in range(len(node_list) - 1):
            node_list[i].left = None  # Remove left child
            node_list[i].right = node_list[i + 1]  # Point right to the next node

        # Last node should have both children as None
        node_list[-1].left = None
        node_list[-1].right = None



if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.right = TreeNode(5)
    root.right.right = TreeNode(6)
    print(Solution().flatten(root))
