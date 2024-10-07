from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        def dfs(node, curr):
            if not node:
                return False

            if node.left == None and node.right == None:
                return (curr + node.val) == targetSum

            curr += node.val
            left = dfs(node.left, curr)
            right = dfs(node.right, curr)
            return left or right


        return dfs(root, 0)

    def hasPathSumIterative(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        stack = [(root, 0)]
        while stack:
            node, curr = stack.pop()
            # if both children are null, then the node is a leaf
            if node.left == None and node.right == None:
                if (curr + node.val) == targetSum:
                    return True

            curr += node.val
            if node.left:
                stack.append((node.left, curr))
            if node.right:
                stack.append((node.right, curr))

        return False



def main():
    rootRightLeft = TreeNode(val=13)
    rootRightRightRight = TreeNode(val=1)
    rootLeftLeftRight = TreeNode(val=2)
    rootLeftLeftLeft = TreeNode(val=7)

    rootLeftLeft = TreeNode(val=11, left = rootLeftLeftLeft, right=rootLeftLeftRight)
    rootLeft = TreeNode(val=4, left=rootLeftLeft)


    rootRightRight = TreeNode(val=4, right=rootRightRightRight)
    rootRight = TreeNode(val=8, left=rootRightLeft, right=rootRightRight)
    root = TreeNode(5, left=rootLeft, right=rootRight)

    solution = Solution()
    targetSum = 22
    print(solution.hasPathSum(root, targetSum))

if __name__ == "__main__":
    main()