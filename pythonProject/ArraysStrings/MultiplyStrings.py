class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        int1 = int(num1)
        int2 = int(num2)
        return str(int1*int2)


if __name__ == '__main__':
    num1 = "2"
    num2 = "3"
    print(Solution().multiply(num1, num2))

