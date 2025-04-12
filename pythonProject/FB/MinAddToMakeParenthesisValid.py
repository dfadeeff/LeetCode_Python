class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        l_count = r_count = added = 0
        for char in s:
            if char == '(':
                l_count += 1
            else:
                if r_count < l_count:
                    r_count += 1
                else:
                    added += 1
        added += l_count - r_count
        return added


if __name__ == '__main__':
    s = "())"
    print(Solution().minAddToMakeValid(s))
    s = "((("
    print(Solution().minAddToMakeValid(s))
