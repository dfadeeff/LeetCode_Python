from typing import List, Optional

from collections import defaultdict, deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        col_map = defaultdict(list)
        queue = deque([(root, 0)])
        min_col = float("inf")
        max_col = float("-inf")

        res = []

        while queue:
            node, col = queue.popleft()
            col_map[col].append(node.val)
            print(col_map)
            min_col = min(min_col, col)
            max_col = max(max_col, col)

            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))
        for level in range(min_col, max_col + 1):
            res.append(col_map[level])

        return res


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().verticalOrder(root))
