from typing import List
from collections import deque


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        """
        Each word = node
        Edge exists if words differ by exactly 1 letter
        Find shortest path from beginWord to endWord

        BFS = shortest path when all edges cost 1
        DFS = finds A path, not necessarily shortest


        Example:
        beginWord = "hit"
        endWord   = "cog"
        wordList  = ["hot","dot","dog","lot","log","cog"]

        word_set = {"hot","dot","dog","lot","log","cog"}

        BFS:
        queue   = [("hit", 1)]   # (word, steps)
        visited = {"hit"}

        ━━━ Level 1: process "hit" ━━━
        generate neighbors:
          _it: not in set
          h_t: "hot" ✅ → add ("hot", 2)
          hi_: not in set
        queue = [("hot", 2)]

        ━━━ Level 2: process "hot" ━━━
        generate neighbors:
          _ot: "dot" ✅, "lot" ✅
          h_t: "hit" visited
          ho_: not in set
        queue = [("dot",3),("lot",3)]

        ━━━ Level 3: process "dot" ━━━
        generate neighbors:
          _ot: "lot" already visited? not yet
          d_t: not in set
          do_: "dog" ✅
        queue = [("lot",3),("lot"...),("dog",4)]

        ━━━ Level 3: process "lot" ━━━
        generate neighbors:
          _ot: "dot" visited
          l_t: not in set
          lo_: "log" ✅
        queue = [("dog",4),("log",4)]

        ━━━ Level 4: process "dog" ━━━
        generate neighbors:
          _og: "log","cog" ✅
          d_g: not in set
          do_: "dot" visited
          "cog" == endWord → return 5 ✅

        """
        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        while queue:
            word, steps = queue.popleft()

            # generate all 1-letter variations

            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = word[:i] + c + word[i + 1:]

                    if new_word == endWord:
                        return steps + 1
                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, steps + 1))

        return 0


if __name__ == "__main__":
    sol = Solution()
    beginWord = "hit"
    endWord = "cog"
    # One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> cog", which is 5 words long.
    wordList = ["hot", "dot", "dog", "lot", "log", "cog"]  # 5
    print(sol.ladderLength(beginWord, endWord, wordList))
