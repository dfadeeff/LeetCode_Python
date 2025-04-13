from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        """
        this variant wants from bottom to top for left view
        and top to bottom for right view

        :param root:
        :return:
        """
        if not root:
            return []
        left_view = []
        right_view = []
        res = []
        queue = deque([root])
        while queue:
            level_len = len(queue)
            for i in range(level_len):
                node = queue.popleft()
                if i == 0:
                    left_view.append(node.val)
                if i == level_len - 1:
                    right_view.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        res.extend(left_view[::-1])
        res.extend(right_view[1:]) #exclude duplicate root
        return res


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(3)
    root.left.right = TreeNode(6)
    root.left.right.right = TreeNode(8)
    root.right = TreeNode(5)
    root.right.left = TreeNode(7)
    root.right.right = TreeNode(9)
    print(Solution().rightSideView(root))
