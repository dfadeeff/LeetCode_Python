from typing import List


class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        if len(s) == 0:
            return 0
        g.sort()
        s.sort()
        cookie, children = 0,0
        ans = 0
        while cookie < len(s) and children < len(g):
            if s[cookie] >= g[children]:
                ans += 1
                cookie += 1
                children += 1
            else:
                cookie += 1

        return ans


if __name__ == '__main__':
    g = [1, 2, 3]
    s = [1, 1]
    print(Solution().findContentChildren(g, s))
    g = [1, 2]
    s = [1, 2, 3]
    print(Solution().findContentChildren(g, s))
    g = [10, 9, 8, 7]
    s = [5, 6, 7, 8]
    print(Solution().findContentChildren(g, s))
