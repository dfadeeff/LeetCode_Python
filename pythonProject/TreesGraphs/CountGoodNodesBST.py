from dns import node

from TreeNode import TreeNode


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, max_so_far):
            if not node:
                return 0
            left = dfs(node.left, max(max_so_far, node.val))
            right = dfs(node.right, max(max_so_far, node.val))
            ans = left + right
            if node.val >= max_so_far:
                ans += 1
            return ans

        return dfs(root, float("-inf"))


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.left.left = TreeNode(3)
    root.right = TreeNode(4)
    root.right.left = TreeNode(1)
    root.right.right = TreeNode(5)
    print(Solution().goodNodes(root))
