from collections import defaultdict, deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
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
        # print("sorted: columns", sorted_columns)
        result = []
        for col in sorted(col_map.keys()):
            # ✅ Sort by row first, then value
            column_nodes = sorted(col_map[col], key=lambda x: (x[0], x[1]))  # here is the difference
            result.append([val for _, val in column_nodes])

        return result


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    result = Solution().verticalTraversal(root)


    def flatten(xss):
        return [x for xs in xss for x in xs]


    print("flat with: ", flatten(result))
    print(result)
    flat_list = []
    for l in result:
        for x in l:
            flat_list.append(x)
    print("flat with: ", flat_list)
