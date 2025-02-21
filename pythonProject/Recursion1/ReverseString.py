from typing import List


class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        index = 0
        length = len(s)
        while index < length/2:
            temp = s[length-1-index]
            s[length-1-index] = s[index]
            s[index] = temp
            index += 1
        return s


if __name__ == "__main__":
    s = ["h", "e", "l", "l", "o"]
    print(Solution().reverseString(s))
    s = ["H", "a", "n", "n", "a", "h"]
    print(Solution().reverseString(s))