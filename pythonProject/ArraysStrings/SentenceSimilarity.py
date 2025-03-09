from typing import List

from black.trans import defaultdict


class Solution:
    def areSentencesSimilar(self, sentence1: List[str], sentence2: List[str], similarPairs: List[List[str]]) -> bool:
        if len(sentence1) != len(sentence2):
            return False

        # Create a set of tuples for quick lookup
        similar_set = set()
        for a, b in similarPairs:
            similar_set.add((a, b))
            similar_set.add((b, a))  # Because similarity is bidirectional

        # Compare each word pair
        for w1, w2 in zip(sentence1, sentence2):
            if w1 == w2:
                continue  # Same word is always similar
            if (w1, w2) not in similar_set:
                return False

        return True


if __name__ == "__main__":
    sentence1 = ["great", "acting", "skills"]
    sentence2 = ["fine", "drama", "talent"]
    similarPairs = [
        ["great", "fine"], ["drama", "acting"], ["skills", "talent"]]
    print(Solution().areSentencesSimilar(sentence1, sentence2, similarPairs))
    sentence1 = ["great", "acting", "skills"]
    sentence2 = ["fine", "painting", "talent"]
    similarPairs = [["great", "fine"], ["drama", "acting"], ["skills", "talent"]]
    print(Solution().areSentencesSimilar(sentence1, sentence2, similarPairs))
