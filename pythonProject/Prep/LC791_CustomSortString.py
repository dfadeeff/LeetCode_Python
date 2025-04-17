from collections import defaultdict


class Solution:
    def customSortString(self, order: str, s: str) -> str:
        s_counts = defaultdict(int)
        string_builder = []

        for char in s:
            s_counts[char] += 1

        for char in order:
            if char in s_counts:
                string_builder.extend([char] * s_counts[char])
                del s_counts[char]

        for k, v in s_counts.items():
            string_builder.extend([k] * v)
        return "".join(string_builder)


if __name__ == '__main__':
    order = "cba"
    s = "abcd"
    print(Solution().customSortString(order, s))
