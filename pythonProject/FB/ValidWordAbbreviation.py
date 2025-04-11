class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        word_pointer = abbr_pointer = 0

        while word_pointer < len(word) and abbr_pointer < len(abbr):
            if abbr[abbr_pointer].isdigit():
                # how many to move forward
                steps = 0
                if abbr[abbr_pointer] == "0":
                    return False
                while abbr_pointer < len(abbr) and abbr[abbr_pointer].isdigit():
                    steps = steps * 10 + int(abbr[abbr_pointer])
                    abbr_pointer += 1
                # now move the word pointer by that amount of steps
                word_pointer += steps

            else:
                if word[word_pointer] != abbr[abbr_pointer]:
                    return False
                else:
                    word_pointer += 1
                    abbr_pointer += 1
        return word_pointer == len(word) and abbr_pointer == len(abbr)

if __name__ == "__main__":
    word = "internationalization"
    abbr = "i12iz4n"
    print(Solution().validWordAbbreviation(word, abbr))
    word = "apple"
    abbr = "a2e"
    print(Solution().validWordAbbreviation(word, abbr))
