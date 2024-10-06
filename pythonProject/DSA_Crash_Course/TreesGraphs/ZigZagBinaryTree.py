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
        ans = [[]]
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
            ans.append(list_to_add)



        ans.remove([])


        for i in range(len(ans)):
            if i % 2 != 0:
                ans[i] = ans[i][::-1]
        return ans


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       3
    #      / \
    #     9   20
    #         / \
    #        15  7
    #
    #
    #

    node15Leaf = TreeNode(15)
    node7Leaf = TreeNode(7)
    node20 = TreeNode(20, left=node15Leaf, right=node7Leaf)
    node9 = TreeNode(9)
    root = TreeNode(3, left=node9, right=node20)
    solution = Solution()
    print(solution.zigzagLevelOrder(root))


if __name__ == '__main__':
    main()
