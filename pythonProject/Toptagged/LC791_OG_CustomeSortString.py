from collections import defaultdict


class Solution:
    def customSortString(self, order: str, s: str) -> str:
        s_counts = defaultdict(int)
        string_builder = []

        for char in s:
            s_counts[char] += 1
        print("s counts", s_counts)

        for char in order:
            if char in s_counts:
                # append `ch` exactly s_counts[ch] times
                string_builder.extend([char] * s_counts[char])
                # remove it from the map so we don’t append it again
                del s_counts[char]
        print("string builder", string_builder)

        for k, v in s_counts.items():
            string_builder.extend([k] * v)
        return "".join(string_builder)


if __name__ == "__main__":
    order = "cba"
    s = "abcd"
    print(Solution().customSortString(order, s))
    # order = "bcafg"
    # s = "abcd"
    # print(Solution().customSortString(order, s))
