from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isCompleteTree(self, root: Optional[TreeNode]) -> bool:
        """BFS traversal"""
        if not root:
            return None
        flag = False
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if not node:
                flag = True
            else:
                if flag:
                    return False
                queue.append(node.left)
                queue.append(node.right)

        return True


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    print(Solution().isCompleteTree(root))
