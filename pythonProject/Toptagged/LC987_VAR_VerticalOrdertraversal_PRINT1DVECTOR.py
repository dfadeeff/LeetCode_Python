# Definition for a binary tree node.
from typing import Optional, List
from collections import deque, defaultdict


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> None:
        if not root:
            return []

        level_items = defaultdict(list)
        queue = deque([(root, 0, 0)])  # store column , row

        # keep track of smallest and largest column
        min_col = float("inf")
        max_col = float("-inf")

        while queue:
            node, row, col = queue.popleft()
            min_col = min(min_col, col)
            max_col = max(max_col, col)

            # here we define value and row, so value is [0] and row is [1], therefore sorting by x[1], x[0]
            level_items[col].append((node.val, row))
            if node.left:
                queue.append((node.left, row + 1, col - 1))
            if node.right:
                queue.append((node.right, row + 1, col + 1))

        res = []

        # include the max value in the range, therefore + 1!!!
        for level in range(min_col, max_col + 1):
            items = level_items[level]
            # sort first by row since row has index 1 in the tuple and node.val is index 0, sort by row first, then value
            items.sort(key=lambda x: (x[1], x[0]))
            # now not interested in the row, just get a value
            items = [val for val, _ in items]
            res.extend(items)
        return res


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().verticalTraversal(root))
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    print(Solution().verticalTraversal(root))
