from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        def dfs(node, path, paths):
            if not node:
                return
            path.append(str(node.val))

            if not node.left and not node.right:
                paths.append('->'.join(map(str, path)))
            dfs(node.left, path, paths)
            dfs(node.right, path, paths)
            path.pop()

        paths = []
        dfs(root, [], paths)

        return paths


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    print(Solution().binaryTreePaths(root))
    root = TreeNode(1)
    print(Solution().binaryTreePaths(root))
