from collections import deque
from lib2to3.btm_utils import reduce_tree
from typing import Optional, List


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        queue = deque([root])
        ans = []

        while queue:
            nodes_in_current_queue = len(queue)
            ans.append(queue[-1].val)
            for _ in range(nodes_in_current_queue):
                node = queue.popleft()
                #ans.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

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

    node5 = TreeNode(5)
    node4 = TreeNode(4)
    node3 = TreeNode(3, right=node4)
    node2 = TreeNode(2, right=node4)
    root = TreeNode(1, left=node2, right=node3)
    solution = Solution()
    print(solution.rightSideView(root))

if __name__ == '__main__':
    main()