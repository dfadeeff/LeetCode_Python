from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        if not root:
            return

        list_nodes = []

        queue = deque([root])


        while queue:
            size = len(queue)
            sum = 0
            for _ in range(size):

                element = queue.popleft()
                sum += element.val

                if element.left:
                    queue.append(element.left)
                if element.right:
                    queue.append(element.right)
            list_nodes.append(sum / size)

        return list_nodes


if __name__ == '__main__':
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().averageOfLevels(root))