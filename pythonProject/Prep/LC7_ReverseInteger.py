class Solution:
    def reverse(self, x: int) -> int:
        is_negative = x < 0
        if is_negative:
            x = -x
        array = [int(digit) for digit in str(x)]

        print(array)
        left = 0
        right = len(array) - 1
        while left < right:
            array[left], array[right] = array[right], array[left]
            left += 1
            right -= 1
        # num = int("".join(map(str, array)))
        num = 0
        for digit in array:
            num = num * 10 + digit
        if is_negative:
            num = -num
        return num if -2 ** (31) < num < 2 ** 31 - 1 else 0

    def reverseEfficient(self, x: int):
        res = 0
        INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1
        sign = -1 if x < 0 else 1
        x = abs(x)
        while x != 0:
            digit = x % 10
            x //= 10

            # Check for overflow before pushing digit
            if res > (INT_MAX - digit) // 10:
                return 0
            res = res * 10 + digit
        return sign * res


if __name__ == "__main__":
    x = 123
    print(Solution().reverse(x))
    print(Solution().reverseEfficient(x))
    x = -123
    print(Solution().reverse(x))
    print(Solution().reverseEfficient(x))
    x = 120
    print(Solution().reverse(x))
    print(Solution().reverseEfficient(x))
    x = 1534236469
    print(Solution().reverse(x))
    print(Solution().reverseEfficient(x))
