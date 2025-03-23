class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, maxSoFar):
            if not node:
                return 0
            left = dfs(node.left, max(maxSoFar, node.val))
            right = dfs(node.right, max(maxSoFar, node.val))
            # number of good nodes in left and right subtree
            ans = left + right
            # add current node if larger than maxSoFar
            if node.val >= maxSoFar:
                ans += 1
            return ans
        return dfs(root, float("-inf"))


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.left.left = TreeNode(3)
    root.right.left = TreeNode(1)
    root.right.right = TreeNode(5)
    print(Solution().goodNodes(root))
