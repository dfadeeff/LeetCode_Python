from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def closestValue(self, root: Optional[TreeNode], target: float) -> int:
        def dfs(node):
            if not node:
                return

            left = dfs(node.left)
            values.append(node.val)
            right = dfs(node.right)

        values = []

        dfs(root)
        print("values:", values)
        minimum = float("inf")
        tuple = [(minimum, 0)]
        for i in range(len(values)):
            minimum = min(minimum, abs(values[i] - target))
            tuple.append((minimum, i))
        print(tuple)
        print("minimum", minimum)
        ans = 0
        for min_value, index in tuple:
            if min_value == minimum:
                ans = index
                break
        return values[ans]

    def closestValueOptimal(self, root: Optional[TreeNode], target: float) -> int:
        def inorder(node):
            return inorder(node.left) + [node.val] + inorder(node.right) if node else []
        return min(inorder(root), key = lambda x: abs(target - x))


def main():
    # Create the binary tree from the example
    # Tree structure:
    #       4
    #      / \
    #     2   5
    #    / \
    #    1  3
    #
    #
    #

    node1Leaf = TreeNode(1)
    node3Leaf = TreeNode(3)
    node5Leaf = TreeNode(5)
    node2 = TreeNode(2, left=node1Leaf, right=node3Leaf)

    root = TreeNode(4, left=node2, right=node5Leaf)
    solution = Solution()
    print(solution.closestValue(root, 3.714286))


if __name__ == '__main__':
    main()
