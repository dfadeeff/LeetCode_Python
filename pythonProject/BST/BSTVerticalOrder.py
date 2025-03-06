from collections import defaultdict, deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        col_map = defaultdict(list)  # Store (row, value) pairs
        queue = deque([(root, 0, 0)])  # (node, column index, row index)

        while queue:
            node, col, row = queue.popleft()
            col_map[col].append((row, node.val))  # Store nodes by (row, value)

            if node.left:
                queue.append((node.left, col - 1, row + 1))  # Move left
            if node.right:
                queue.append((node.right, col + 1, row + 1))  # Move right

        # Sort columns based on index
        sorted_columns = sorted(col_map.keys())

        result = []
        for col in sorted_columns:
            # Sort by row index, and then by value for tie-breaking
            column_nodes = sorted(col_map[col], key=lambda x: x[0])
            result.append([val for _, val in column_nodes])

        return result

if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().verticalOrder(root))