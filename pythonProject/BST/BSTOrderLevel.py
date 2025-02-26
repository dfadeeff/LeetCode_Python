from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        nodes_list = []
        if not root:
            return nodes_list

        queue = deque([root])
        while queue:
            size = len(queue)
            nodes_at_level = []
            for _ in range(size):
                element = queue.popleft()
                if element.left:
                    queue.append(element.left)
                if element.right:
                    queue.append(element.right)
                nodes_at_level.append(element.val)
            nodes_list.append(nodes_at_level)
        return nodes_list


if __name__ == '__main__':
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().levelOrder(root))
