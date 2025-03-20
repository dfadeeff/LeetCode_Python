from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
        left_leaves = []
        def dfs(node, is_left):
            if not node:
                return 0
            if not node.left and not node.right and is_left:
                left_leaves.append(node.val)
            dfs(node.left, is_left=True)
            dfs(node.right, is_left=False)

        dfs(root, is_left=False)
        #print(left_leaves)
        return sum(left_leaves)


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().sumOfLeftLeaves(root))

