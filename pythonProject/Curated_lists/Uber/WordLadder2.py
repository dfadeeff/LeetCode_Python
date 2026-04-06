from typing import List

from collections import defaultdict, deque


class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        """
        BFS → build DAG → backtrack → return all paths

        1. BFS to find shortest distance AND build parent map
        2. Backtrack through parent map to reconstruct all paths

        Phase 1: BFS
          Find shortest distance
          For each word, track ALL parents that reach it optimally
          parents[word] = set of words that lead to word in min steps

        Phase 2: Backtracking
          Start from endWord
          Follow parents back to beginWord
          Each path = one valid shortest transformation



        Word Ladder II extends I with two additions:

        1. Instead of stopping at endWord,
           I finish the entire BFS level
           → captures ALL parents at each level

        2. After BFS, backtrack from endWord
           following parents map back to beginWord
           → reconstructs all shortest paths

        The trick: add level_visited AFTER processing each level
                   not during — otherwise siblings block each other
                   from sharing multiple parents

        """

        word_set = set(wordList)
        if endWord not in word_set:
            return []

        # Phase 1: BFS — build parents map
        parents = defaultdict(set)
        visited = {beginWord}
        queue = deque([beginWord])
        found = False

        while queue and not found:
            # process one level at a time
            level_visited = set()

            for _ in range(len(queue)):
                word = queue.popleft()

                for i in range(len(word)):
                    for c in 'abcdefghijklmnopqrstuvwxyz':
                        new_word = word[:i] + c + word[i + 1:]

                        if new_word not in word_set:
                            continue
                        if new_word in visited:
                            continue

                        # valid neighbor at next level
                        parents[new_word].add(word)
                        level_visited.add(new_word)

                        if new_word == endWord:
                            found = True  # don't stop yet!
                            # finish this level

            # add entire level to visited AFTER processing
            visited |= level_visited
            queue.extend(level_visited)

        if not found:
            return []

        # Phase 2: Backtrack from endWord to beginWord
        result = []

        def backtrack(word, path):
            if word == beginWord:
                result.append(list(reversed(path)))
                return
            for parent in parents[word]:
                path.append(parent)
                backtrack(parent, path)
                path.pop()

        backtrack(endWord, [endWord])
        return result


if __name__ == "__main__":
    sol = Solution()
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot", "dot", "dog", "lot", "log", "cog"]
    print(sol.findLadders(beginWord, endWord, wordList))
