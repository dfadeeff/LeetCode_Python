from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def findLeaves(self, root: Optional[TreeNode]) -> List[List[int]]:
        def dfs(node):
            if not node:
                return -1  # base case (below leaf)

            left_height = dfs(node.left)
            right_height = dfs(node.right)

            current_height = 1 + max(left_height, right_height)

            # Extend result list if needed
            if len(result) == current_height:
                result.append([])

            # append node value at its height-level
            result[current_height].append(node.val)

            return current_height

        result = []
        dfs(root)
        return result


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    print(Solution().findLeaves(root))
