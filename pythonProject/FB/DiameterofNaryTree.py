from typing import Optional, List


class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children if children is not None else []


class Solution:
    def diameter(self, root: 'Node') -> int:
        """
        :type root: 'Node'
        :rtype: int
        """
        if not root:
            return 0
        diameter = 0

        def dfs(node):
            nonlocal diameter
            if not node:
                return 0

            # Store top two longest depths among children
            first, second = 0, 0

            max_diameter = float('-inf')
            for child in node.children:
                depth = dfs(child)
                if depth > first:
                    second = first
                    first = depth
                elif depth > second:
                    second = depth
            # update global
            diameter = max(diameter, second + first)
            return first + 1

        dfs(root)
        return diameter


if __name__ == '__main__':
    # Tree:
    #         1
    #     /   |  \
    #     2   3   4
    #        / \
    #       5   6

    node5 = Node(5)
    node6 = Node(6)
    node3 = Node(3, [node5, node6])
    node2 = Node(2)
    node4 = Node(4)
    root = Node(1, [node2, node3, node4])
    print(Solution().diameter(root))
