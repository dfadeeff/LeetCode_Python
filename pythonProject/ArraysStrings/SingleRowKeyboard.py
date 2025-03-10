from black.trans import defaultdict


class Solution:
    def calculateTime(self, keyboard: str, word: str) -> int:
        hashmapIndex = defaultdict(int)
        for i, number in enumerate(keyboard):
            hashmapIndex[number] += i
        print(hashmapIndex)

        sum_time = hashmapIndex[word[0]]
        for i in range(1,len(word)):
            sum_time += abs(hashmapIndex[word[i]] - hashmapIndex[word[i-1]])

        return sum_time


if __name__ == '__main__':
    keyboard = "abcdefghijklmnopqrstuvwxyz"
    word = "cba"
    print(Solution().calculateTime(keyboard, word))
