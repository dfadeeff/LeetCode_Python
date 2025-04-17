class Solution:
    def addStringsNaive(self, num1: str, num2: str) -> str:
        curr1 = curr2 = 0
        for char in num1:
            if char.isdigit():
                curr1 = curr1 * 10 + int(char)
        for char in num2:
            if char.isdigit():
                curr2 = curr2 * 10 + int(char)

        return str(curr1+curr2)

    def addStrings(self, num1: str, num2: str) -> str:
        res = []

        carry = 0
        p1 = len(num1) - 1
        p2 = len(num2) - 1
        while p1 >= 0 or p2 >= 0:
            x1 = ord(num1[p1]) - ord('0') if p1 >= 0 else 0
            x2 = ord(num2[p2]) - ord('0') if p2 >= 0 else 0
            value = (x1 + x2 + carry) % 10
            carry = (x1 + x2 + carry) // 10
            res.append(value)
            p1 -= 1
            p2 -= 1
            print("x1", x1)
            print("x2", x2)

        if carry:
            res.append(carry)

        return ''.join(str(x) for x in res[::-1])

if __name__ == "__main__":
    num1 = "456"
    num2 = "77"
    print(Solution().addStrings(num1,num2))