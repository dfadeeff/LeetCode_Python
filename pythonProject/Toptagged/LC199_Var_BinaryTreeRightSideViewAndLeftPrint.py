from typing import Optional, List
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]):
        if not root:
            return []
        queue = deque([root])
        left_view = []
        right_view = []

        while queue:
            size = len(queue)
            for i in range(size):
                node = queue.popleft()
                if i == 0:
                    left_view.append(node.val)
                if i == size - 1:
                    right_view.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        for i in left_view[::-1]:
            print(i)
        for i in right_view[1:]:
            print(i)



if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(3)
    root.right = TreeNode(5)
    root.left.right = TreeNode(6)
    root.left.right.right = TreeNode(8)
    root.right.left = TreeNode(7)
    root.right.right = TreeNode(9)

    print(Solution().rightSideView(root))
