class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def treeSum(self, root: TreeNode) -> int:
        if not root:
            return 0
        left = self.treeSum(root.left)
        right = self.treeSum(root.right)
        return root.val + left + right


if __name__ == '__main__':
    root = TreeNode(5)
    root.left = TreeNode(11)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(8)
    root.right = TreeNode(3)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(12)
    print(Solution().treeSum(root))
