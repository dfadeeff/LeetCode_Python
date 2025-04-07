from typing import List


class Solution:
    def findStrobogrammatic(self, n: int) -> List[str]:
        def helper(n: int, total: int) -> List[str]:
            if n == 0:
                return [""]
            if n == 1:
                return ["0", "1", "8"]  # Correct base case
            middles = helper(n - 2, total)
            result = []
            for middle in middles:
                # Iterate over all valid pairs.
                for a, b in [("0", "0"), ("1", "1"), ("6", "9"), ("8", "8"), ("9", "6")]:
                    # Don't allow numbers with leading zeros.
                    if n == total and a == "0":
                        continue
                    result.append(a + middle + b)
            return result  # Moved return outside the for loop

        return helper(n, n)


if __name__ == "__main__":
    print(Solution().findStrobogrammatic(2))  # Example: Output might be ["11", "69", "88", "96"]
    print(Solution().findStrobogrammatic(
        3))  # Example: Output might be ["101", "609", "808", "906", "111", "619", "818", "916", "181", "689", "888", "986"]
