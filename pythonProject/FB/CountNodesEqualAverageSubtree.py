class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        self.count = 0

        def dfs(node):
            if not node:
                return (0, 0)  # (sum, count)

            left_sum, left_count = dfs(node.left)
            right_sum, right_count = dfs(node.right)

            total_sum = left_sum + right_sum + node.val
            total_count = left_count + right_count + 1

            if node.val == total_sum // total_count:
                self.count += 1

            return (total_sum, total_count)

        dfs(root)
        return self.count


if __name__ == '__main__':
    root = TreeNode(4)
    root.left = TreeNode(8)
    root.right = TreeNode(5)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(1)
    root.right.right = TreeNode(6)
    print(Solution().averageOfSubtree(root))
