from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def getMinimumDifferenceBFS(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        ans = []
        queue = deque([root])
        while queue:
            current_level = len(queue)
            print("current level", current_level)
            for _ in range(current_level):
                node = queue.popleft()
                print(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                ans.append(node.val)
        ans = sorted(ans)
        minimunm = float("inf")
        for i in range(len(ans)):
            for j in range(i+1, len(ans)):
                minimunm = min(ans[j]-ans[i], minimunm)
        print(ans)
        return minimunm

    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return

            left = dfs(node.left)
            values.append(node.val)
            right = dfs(node.right)

        values = []
        dfs(root)
        ans = float("inf")
        for i in range(1, len(values)):
            ans = min(ans, values[i] - values[i - 1])

        return ans


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       4
    #      / \
    #     2   6
    #    / \
    #    1  3
    #
    #
    #

    node1Leaf = TreeNode(1)
    node3Leaf = TreeNode(3)
    node6Leaf = TreeNode(6)
    node2 = TreeNode(2, left=node1Leaf, right=node3Leaf)

    root = TreeNode(4, left=node2, right=node6Leaf)
    solution = Solution()
    print(solution.getMinimumDifferenceBFS(root))
    print(solution.getMinimumDifference(root))


if __name__ == '__main__':
    main()
