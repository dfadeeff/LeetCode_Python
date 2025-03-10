class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        """bijection therefore 2 hashmaps"""
        words = s.split()
        if len(pattern) != len(words):
            return False

        p_to_w = {}
        w_to_p = {}

        for p, w in zip(pattern, words):
            if p in p_to_w:
                if p_to_w[p] != w:
                    return False
            else:
                p_to_w[p] = w

            if w in w_to_p:
                if w_to_p[w] != p:
                    return False
            else:
                w_to_p[w] = p
        print(p_to_w)
        print(w_to_p)
        return True


if __name__ == '__main__':
    pattern = "abba"
    s = "dog cat cat dog"
    print(Solution().wordPattern(pattern, s))
    pattern = "abba"
    s = "dog cat cat fish"
    print(Solution().wordPattern(pattern, s))
    pattern = "abba"
    s = "dog dog dog dog"
    print(Solution().wordPattern(pattern, s))
