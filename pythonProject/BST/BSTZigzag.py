# Definition for a binary tree node.
from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        answer = []
        queue = deque([root])
        while queue:
            current_level = len(queue)
            print("current level", current_level)
            list_to_add = []
            for _ in range(current_level):
                node = queue.popleft()
                print(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                list_to_add.append(node.val)
            answer.append(list_to_add)
        print("current answer:", answer)
        for i in range(len(answer)):
            if i % 2 != 0:
                answer[i] = answer[i][::-1]
        return answer


if __name__ == '__main__':
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().zigzagLevelOrder(root))
