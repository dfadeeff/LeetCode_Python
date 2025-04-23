class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        nums1 = num1.split('.')
        nums2 = num2.split('.')
        decimals1 = nums1[1] if len(nums1) > 1 else ''
        decimals2 = nums2[1] if len(nums2) > 1 else ''

        max_len = max(len(decimals1), len(decimals2))

        # .ljust(width, '0') is a Python string method that,
        # if the string is shorter than width, pads on the right with the given character (here '0')
        # until it reaches exactly width.
        decimals1 = decimals1.ljust(max_len, '0')
        decimals2 = decimals2.ljust(max_len, '0')

        carry = [0]
        result = []

        def add_strings_415(num1: str, num2: str, carry: list) -> str:
            n1 = len(num1) - 1
            n2 = len(num2) - 1
            result = []
            while n1 >= 0 or n2 >= 0:
                sum = 0
                if n1 >= 0:
                    sum += int(num1[n1])
                    n1 -= 1
                if n2 >= 0:
                    sum += int(num2[n2])
                    n2 -= 1
                sum += carry[0]

                result.append(str(sum % 10))
                carry[0] = sum // 10

            return ''.join(result)

        result.append(add_strings_415(decimals1, decimals2, carry))

        if decimals1 or decimals2:
            result.append('.')

        result.append(add_strings_415(nums1[0], nums2[0], carry))
        if carry[0]:
            # print(carry)
            result.append(str(carry[0]))
        return "".join(result)[::-1]


if __name__ == "__main__":
    num1 = "11.11"
    num2 = "123.5"
    print(Solution().addStrings(num1, num2))
    num1 = "9."
    num2 = "9.4"
    print(Solution().addStrings(num1, num2))
