# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def str2tree(self, s: str) -> Optional[TreeNode]:
        """parse from left to right, """
        if not s:
            return None
        stack = []
        i = 0
        while i < len(s):
            cur_char = s[i]

            if cur_char == "-":
                i += 1
                val = 0
                while i < len(s) and s[i].isdigit():
                    val = val * 10 + int(s[i])

                    # increase the index once we parse
                    i += 1
                i -= 1
                stack.append(TreeNode(-val))

            elif cur_char.isdigit():
                val = 0
                while i < len(s) and s[i].isdigit():
                    val = val * 10 + int(s[i])
                    i += 1
                i -= 1
                stack.append(TreeNode(val))
            elif cur_char == ")":
                top = stack.pop()
                if not stack[-1].left:
                    stack[-1].left = top
                else:
                    stack[-1].right = top
            i += 1
        return stack[-1]



if __name__ == "__main__":
    s = "4(2(3)(1))(6(5))"
    print(Solution().str2tree(s))
    s = "4(2(3)(1))(6(5)(7))"
    print(Solution().str2tree(s))
