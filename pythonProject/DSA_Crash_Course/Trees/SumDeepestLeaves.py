from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def deepestLeavesSum(self, root: Optional[TreeNode]) -> int:
        if not root:
            return []
        queue = deque([root])

        while queue:
            current_level = len(queue)
            #print("current level", current_level)
            sum = 0
            for _ in range(current_level):

                node = queue.popleft()
                print(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                sum += node.val
        return sum



def main():
    # Create the binary tree from the example
    # Tree structure:
    #       1
    #      / \
    #     2   3
    #    / \    \
    #    4   5    6
    #   /           \
    #   7           8
    #

    node7Leaf = TreeNode(7)
    node8Leaf = TreeNode(8)
    node4 = TreeNode(4, left=node7Leaf)
    node5 = TreeNode(5)
    node6 = TreeNode(6, right=node8Leaf)

    node2 = TreeNode(3, left=node4, right=node5)
    node3 = TreeNode(2, right=node6)
    root = TreeNode(1, left=node2, right=node3)
    solution = Solution()
    print(solution.deepestLeavesSum(root))

if __name__ == '__main__':
    main()

