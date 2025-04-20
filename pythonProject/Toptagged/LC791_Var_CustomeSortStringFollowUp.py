from collections import defaultdict


class Solution:
    def customSortString(self, order: str, s: str) -> str:
        # 1) Build frequency array for s
        freq = [0] * 26
        base = ord('a')  # base is ord(a) = 97
        for ch in s:
            freq[ord(ch) - base] += 1
        print(freq)
        # 2) Output every character in `order` as many times as it appears
        res = []
        for ch in order:
            idx = ord(ch) - base
            if freq[idx] > 0:
                # append ch freq[idx] times
                res.append(ch * freq[idx])
                freq[idx] = 0  # mark as emitted

        # 3) Append any remaining characters (in ‘a’→‘z’ order)
        for i in range(26):
            if freq[i] > 0:
                res.append(chr(base + i) * freq[i])

        return "".join(res)


if __name__ == "__main__":
    order = ["c", "b", "a"]
    s = "abcd"
    print(Solution().customSortString(order, s))
    # order = "bcafg"
    # s = "abcd"
    # print(Solution().customSortString(order, s))
