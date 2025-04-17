from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumNumbersPaths(self, root: Optional[TreeNode]) -> int:
        def dfs(node, path, paths):
            if not node:
                return
            # Add current node's value to the path
            path.append(node.val)
            if not node.left and not node.right:
                paths.append(list(path))
            dfs(node.left, path, paths)
            dfs(node.right, path, paths)

            # Backtrack (remove last node to explore other paths)
            path.pop()

        paths = []  # Store all root-to-leaf paths
        dfs(root, [], paths)

        sum = 0
        for path in paths:
            new_join = ''.join(map(str, path))
            new_int = int(new_join)
            sum += new_int
        return sum

    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def dfs(node, current_number):
            if not node:
                return 0
            current_number = current_number * 10 + node.val

            # if leaf, return the number formed
            if not node.left and not node.right:
                return current_number
            #otherwise, recurse on both children
            left_sum = dfs(node.left, current_number)
            right_sum = dfs(node.right, current_number)
            return left_sum + right_sum

        return dfs(root, 0)

if __name__ == '__main__':
    root = TreeNode(4)
    root.left = TreeNode(9)
    root.right = TreeNode(0)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(1)
    print(Solution().sumNumbers(root))