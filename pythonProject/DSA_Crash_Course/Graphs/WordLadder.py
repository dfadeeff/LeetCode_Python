from collections import deque
from typing import List


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        wordListset = set(wordList)
        def generate_neighbors(word: str, valid_words: List[str]) -> List[str]:
            """
            Generate all possible neighbors of the given word by changing one letter at a time.
            Each neighbor must be in the valid_words list (which acts like a dictionary or bank).

            Args:
            - word (str): The current word.
            - valid_words (List[str]): A list of valid words (or genes) that can be neighbors.

            Returns:
            - List[str]: A list of neighboring words that differ by exactly one letter.
            """
            neighbors = []
            word_len = len(word)

            # Iterate over each position in the word
            for i in range(word_len):
                # For each position, try changing the character to any other valid letter (a-z)
                for char in 'abcdefghijklmnopqrstuvwxyz':  # For general words
                    if word[i] != char:
                        # Create a new neighbor by replacing the i-th character
                        neighbor = word[:i] + char + word[i + 1:]

                        # Only add it if it's a valid word in the valid_words list
                        if neighbor in valid_words:
                            neighbors.append(neighbor)

            return neighbors

        if endWord not in wordList:
            return 0  # Return 0 if endWord is not in the wordList (since no transformation is possible)

        queue = deque([(beginWord, 1)])  # Start BFS with depth 1 (including the first word)
        seen = set()
        seen.add(beginWord)

        while queue:
            node, steps = queue.popleft()

            if node == endWord:
                return steps  # Found the shortest path to the endWord

            for neighbor in generate_neighbors(node, wordListset):  # Pass wordList as the second argument
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append((neighbor, steps + 1))

        return 0  # If no valid transformation is found, return 0


def main():
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot", "dot", "dog", "lot", "log", "cog"]
    print(Solution().ladderLength(beginWord, endWord, wordList))  # Output: 5


if __name__ == "__main__":
    main()