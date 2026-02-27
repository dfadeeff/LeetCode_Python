class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_sorted = tuple(sorted(s))
        t_sorted = tuple(sorted(t))
        return s_sorted == t_sorted


if __name__ == "__main__":
    solution = Solution()
    s = "racecar"
    t = "carrace"
    print(solution.isAnagram(s, t))
    s = "jar"
    t = "jam"
    print(solution.isAnagram(s, t))
