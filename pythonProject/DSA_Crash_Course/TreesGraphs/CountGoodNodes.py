class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, max_so_far):
            if not node:
                return 0

            left = dfs(node.left, max(max_so_far, node.val))
            right = dfs(node.right, max(max_so_far, node.val))
            ans = left + right
            if node.val >= max_so_far:
                ans += 1

            return ans

        return dfs(root, float("-inf"))

def main():
    rootLeftLeft = TreeNode(3)
    rootLeft = TreeNode(1, left=rootLeftLeft)
    rootRightLeft = TreeNode(1)
    rootRighRight = TreeNode(5)
    rootRight = TreeNode(4, left=rootRightLeft, right=rootRighRight)

    root = TreeNode(3, left=rootLeft, right=rootRight)

    solution = Solution()
    print(solution.goodNodes(root))

if __name__ == "__main__":
    main()