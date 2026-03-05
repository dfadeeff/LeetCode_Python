from typing import List

from collections import defaultdict


class Solution:
    def countPalindromePaths(self, parent: List[int], s: str) -> int:
        """
        Why This Works — The Logic Chain
    ```
    We want: pairs where path letters can form palindrome
             ↓
    Palindrome rearrangement: at most 1 letter has odd count
             ↓
    Odd/even tracking: use XOR bitmask
             ↓
    Path bitmask: mask[u] XOR mask[v] (shared part cancels)
             ↓
    Palindrome condition: XOR result is 0 or has 1 bit set
             ↓
    Counting: for each node, look up how many previous nodes
              have matching or 1-bit-different masks
            :param parent:
            :param s:
            :return:
        """
        n = len(parent)

        # ---- STEP 1: BUILD TREE ----
        children = defaultdict(list)
        for i in range(1, n):
            children[parent[i]].append(i)

        # ---- STEP 2: COMPUTE MASKS WITH DFS ----
        mask = [0] * n
        # Using iterative DFS to avoid stack overflow for large n
        stack = [0]
        visited = [False] * n
        visited[0] = True

        while stack:
            node = stack.pop()
            for child in children[node]:
                if not visited[child]:
                    visited[child] = True
                    # XOR parent's mask with this edge's letter
                    bit = ord(s[child]) - ord('a')
                    mask[child] = mask[node] ^ (1 << bit)
                    stack.append(child)

        # ---- STEP 3: COUNT PAIRS ----
        counter = defaultdict(int)
        result = 0

        for i in range(n):
            m = mask[i]

            # Case 1: same mask → XOR = 0 → palindrome

            result += counter[m]

            # Case 2: differ by 1 bit → XOR has 1 bit set → palindrome
            for bit in range(26):
                result += counter[m ^ (1 << bit)]

            # Add current mask to counter AFTER checking
            # (this prevents counting a node with itself)
            counter[m] += 1

        return result


if __name__ == "__main__":
    sol = Solution()
    parent = [-1, 0, 0, 1, 1, 2]
    s = "acaabc"
    print(sol.countPalindromePaths(parent, s))
