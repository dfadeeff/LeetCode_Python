class Solution:
    def reverseWords(self, s: str) -> str:
        cleaned_s = " ".join(s.split())

        string_array = []
        for i in cleaned_s.split():
            string_array.append(i)

        left = 0
        right = len(string_array) - 1
        while left < right:
            string_array[left], string_array[right] = string_array[right], string_array[left]
            left += 1
            right -= 1
        return " ".join(string_array)


if __name__ == '__main__':
    s = "the sky is blue"
    print(Solution().reverseWords(s))
