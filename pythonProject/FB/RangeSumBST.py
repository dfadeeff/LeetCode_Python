from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rangeSumBSTNaive(self, root: Optional[TreeNode], low: int, high: int) -> int:
        nodes = []

        def dfs(node):
            if not node:
                return None
            nodes.append(node.val)
            dfs(node.left)
            dfs(node.right)

        dfs(root)

        range_sum = 0
        for num in nodes:
            if low <= num <= high:
                range_sum += num
        return range_sum

    def rangeSumBSTOptimalIterative(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if not root:
            return 0
        ans = 0
        stack = [root]
        while stack:
            node = stack.pop()

            if node:
                if low <= node.val <= high:
                    ans += node.val
                if low < node.val:
                    stack.append(node.left)
                if node.val < high:
                    stack.append(node.right)

        return ans

    def rangeSumBSTOptimalRecursive(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if not root:
            return 0
        range_sum = 0

        def dfs(node, low, high):
            nonlocal range_sum
            if node:
                if low <= node.val <= high:
                    range_sum += node.val
                if low < node.val:
                    dfs(node.left, low, high)
                if node.val < high:
                    dfs(node.right, low, high)

        dfs(root, low, high)
        return range_sum


if __name__ == '__main__':
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(7)
    root.right.right = TreeNode(18)
    low = 7
    high = 15
    print(Solution().rangeSumBSTNaive(root, low, high))
