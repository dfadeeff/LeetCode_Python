from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def largestValues(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        ans = []
        queue = deque([root])

        while queue:
            nodes_in_current_queue = len(queue)
            max = float("-inf")
            for _ in range(nodes_in_current_queue):

                node = queue.popleft()
                if max < node.val:
                    max = node.val

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            ans.append(max)
        return ans


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       1
    #      / \
    #     2   3
    #      \    \
    #       5    4
    #
    #
    #

    node5Leaf = TreeNode(5)
    node3Leaf = TreeNode(3)
    node9Leaf = TreeNode(9)

    node3 = TreeNode(3, left=node5Leaf, right=node3Leaf)
    node2 = TreeNode(2, right=node9Leaf)
    root = TreeNode(1, left=node3, right=node2)
    solution = Solution()
    print(solution.largestValues(root))


if __name__ == '__main__':
    main()
