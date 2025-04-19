import re


class Solution:
    def countAndSay(self, n: int) -> str:
        current_string = "1"
        for _ in range(n - 1):
            next_string = ""
            j = 0
            k = 0
            while j < len(current_string):
                while (
                    k < len(current_string)
                    and current_string[k] == current_string[j]
                ):
                    k += 1
                next_string += str(k - j) + current_string[j]
                j = k
            current_string = next_string
        return current_string

    def countAndSayRegex(self, n: int) -> str:
        s = "1"
        for _ in range(n - 1):
            # m.group(0) is the entire match, m.group(1) is its first digit
            s = re.sub(
                r"(.)\1*", lambda m: str(len(m.group(0))) + m.group(1), s
            )
        return s


if __name__ == "__main__":
    n = 4
    print(Solution().countAndSay(n))
    print(Solution().countAndSayRegex(n))
    n = 1
    print(Solution().countAndSay(n))
    print(Solution().countAndSayRegex(n))
