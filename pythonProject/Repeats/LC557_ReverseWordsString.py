class Solution:
    def reverseWords(self, s: str) -> str:
        ans_str = []
        parts = s.split()
        for i in parts:
            reversed = self.reverseString(i)
            ans_str.append(reversed)
        return " ".join(ans_str)

    def reverseString(self, s):
        s_list = list(s)
        left = 0
        right = len(s) - 1
        while left < right:
            s_list[left], s_list[right] = s_list[right], s_list[left]
            left += 1
            right -= 1
        s = ''.join(s_list)
        return s


if __name__ == "__main__":
    s = "Let's take LeetCode contest"
    print(Solution().reverseWords(s))
