class Solution:
    def convert(self, num):
        s = str(num)
        n = len(s)
        l, r = (n - 1) // 2, n // 2
        s_list = list(s)

        while l >= 0:
            s_list[r] = s_list[l]
            r += 1
            l -= 1
        return int("".join(s_list))

    def previous_palindrome(self, num):
        left, right = 0, num
        ans = float("-inf")
        while left <= right:
            mid = (right - left) // 2 + left
            palin = self.convert(mid)
            if palin < num:
                ans = palin
                left = mid + 1
            else:
                right = mid - 1
        return ans

    def next_palindrome(self, num):
        left, right = 0, int(1e18)
        ans = float("-inf")
        while left <= right:
            mid = (right - left) // 2 + left
            palin = self.convert(mid)
            if palin > num:
                ans = palin
                right = mid - 1
            else:
                left = mid + 1
        return ans

    def nearestPalindromic(self, n: str) -> str:
        num = int(n)
        a = self.previous_palindrome(num)
        b = self.next_palindrome(num)
        if abs(a - num) <= abs(b - num):
            return str(a)
        return str(b)


if __name__ == "__main__":
    sol = Solution()
    n = "123"
    print(sol.nearestPalindromic(n))
    n = "1"
    print(sol.nearestPalindromic(n))
