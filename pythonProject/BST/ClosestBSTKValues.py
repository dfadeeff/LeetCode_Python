from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def closestKValues(self, root: Optional[TreeNode], target: float, k: int) -> List[int]:
        nodes = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            nodes.append(node.val)
            dfs(node.right)
        dfs(root)
        nodes.sort(key=lambda x: abs(x - target))
        return nodes[:k]
if __name__ == "__main__":
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(5)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    target = 3.714286
    k = 2
    print(Solution().closestKValues(root, target, 2))
