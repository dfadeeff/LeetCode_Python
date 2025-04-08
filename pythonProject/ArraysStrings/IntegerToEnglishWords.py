class Solution:
    def numberToWords(self, num: int) -> str:
        """"
        1. Break number into groups of 3 digits, from the right.
        2. Convert each group to words.
        3. Add scale names (“Thousand”, “Million”, “Billion”, etc.)
        4. Assemble.

        """
        if num == 0:
            return "Zero"

        below_20 = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                    "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
                    "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        thousands = ["", "Thousand", "Million", "Billion"]

        # Helper to convert num < 1000
        def helper(n):
            if n == 0:
                return ""
            elif n < 20:
                return below_20[n] + " "
            elif n < 100:
                return tens[n // 10] + " " + helper(n % 10)
            else:
                return below_20[n // 100] + " Hundred " + helper(n % 100)

        res = ""
        for idx, scale in enumerate(thousands):
            if num % 1000 != 0:
                res = helper(num % 1000) + scale + " " + res
            num //= 1000

        return res.strip()


if __name__ == "__main__":
    num = 12345
    print(Solution().numberToWords(num))
