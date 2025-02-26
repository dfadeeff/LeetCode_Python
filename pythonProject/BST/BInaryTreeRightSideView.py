import collections

from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        list_nodes = []
        queue = collections.deque([root])

        while queue:
            size = len(queue)
            list_at_level = []
            for _ in range(size):
                element = queue.popleft()
                list_at_level.append(element.val)
                if element.left:
                    queue.append(element.left)
                if element.right:
                    queue.append(element.right)
            list_nodes.append(list_at_level)

        final_answer = []
        for level in list_nodes:
            final_answer.append(level[-1])

        return final_answer


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(4)
    print(Solution().rightSideView(root))
