class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:

        if len(s1) > len(s2):
            return False

        s1Count, s2Count = [0] * 26, [0] * 26

        for i in range(len(s1)):
            s1Count[ord(s1[i]) - ord("a")] += 1
            s2Count[ord(s2[i]) - ord("a")] += 1

        for i in range(len(s2) - len(s1)):
            """
            Each iteration:
            1.	Compare s1Count with current s2Count
            2.	Slide the window by 1:
            •	Add the next character (s2[i + len(s1)])
            •	Remove the leftmost character (s2[i])
            """

            if s1Count == s2Count:
                return True
            # slide window: add new char on the right
            s2Count[ord(s2[i + len(s1)]) - ord("a")] += 1
            # remove left-most char
            s2Count[ord(s2[i]) - ord("a")] -= 1

        return s1Count == s2Count


if __name__ == "__main__":
    s1 = "ab"
    s2 = "eidbaooo"
    print(Solution().checkInclusion(s1, s2))
