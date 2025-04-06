class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        w, a = 0, 0

        while w < len(word) and a < len(abbr):
            if abbr[a].isalpha():
                if word[w] != abbr[a]:
                    return False
                w += 1
                a += 1
            else:
                if abbr[a] == '0':
                    return False  # no leading zeros!
                num = 0
                while a < len(abbr) and abbr[a].isdigit():
                    num = num * 10 + int(abbr[a])
                    a += 1
                w += num

        return w == len(word) and a == len(abbr)


if __name__ == '__main__':
    word = "internationalization"
    abbr = "i12iz4n"
    print(Solution().validWordAbbreviation(word, abbr))
