from collections import deque
from typing import List


class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:

        def gene_neighbors(gene):
            """
            Generate all possible gene strings that differ by exactly one character.

            Args:
            - gene (str): The current gene string.

            Returns:
            - List[str]: A list of neighboring gene strings.
            """
            ans = []
            genes = ['A', 'C', 'G', 'T']
            for i in range(len(gene)):
                for g in genes:
                    if g != gene[i]:
                        # Replace the character at position i with g
                        neighbor = gene[:i] + g + gene[i + 1:]
                        ans.append(neighbor)
            return ans

        queue = deque([(startGene, 0)])
        seen = set()
        seen.add(startGene)

        while queue:
            node, steps = queue.popleft()
            if node == endGene :
                return steps

            for neighbor in gene_neighbors(node):
                if neighbor not in seen and neighbor in bank:
                    seen.add(neighbor)
                    queue.append((neighbor, steps + 1))

        return -1


def main():
    startGene = "AACCGGTT"
    endGene = "AACCGGTA"
    bank = ["AACCGGTA"]
    print(Solution().minMutation(startGene, endGene, bank))

    startGene = "AACCGGTT"
    endGene = "AAACGGTA"
    bank = ["AACCGGTA", "AACCGCTA", "AAACGGTA"]
    print(Solution().minMutation(startGene, endGene, bank))

    startGene = "AACCTTGG"
    endGene = "AATTCCGG"
    bank = ["AATTCCGG", "AACCTGGG", "AACCCCGG", "AACCTACC"]
    print(Solution().minMutation(startGene, endGene, bank))


if __name__ == '__main__':
    main()
