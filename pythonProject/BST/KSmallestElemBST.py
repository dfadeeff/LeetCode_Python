from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        list_nodes = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            list_nodes.append(node.val)
            dfs(node.right)
        dfs(root)
        list_nodes.sort()
        answer = 0
        for i in range(0,len(list_nodes)):
            if k-1 == i:
                answer = list_nodes[i]
                break
        return answer



if __name__ == '__main__':
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.left.right = TreeNode(2)
    root.right = TreeNode(4)
    print(Solution().kthSmallest(root, 1))