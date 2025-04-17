class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        x = abs(x)
        array = [int(digit) for digit in str(x)]
        left = 0
        right = len(array) - 1
        while left < right:
            if array[left] != array[right]:
                return False
            left += 1
            right -= 1

        return True

if __name__ == "__main__":
    x = -121
    print(Solution().isPalindrome(x))
    x = 121
    print(Solution().isPalindrome(x))