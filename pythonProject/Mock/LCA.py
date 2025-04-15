class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None




class Solution:
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        a,b = p,q
        while a!=b:
            a = a.parent if a.parent else q
            b = b.parent if b.parent else p
        return a


if __name__ == '__main__':
    root = Node(1)
    root.left = Node(5)
    root.right = Node(1)
    root.left.left = Node(6)
    root.left.right = Node(2)
    root.left.right.left = Node(7)
    root.left.right.right = Node(4)
    root.right.left = Node(0)
    root.right.right = Node(8)
    print(Solution().lowestCommonAncestor(root,root))
