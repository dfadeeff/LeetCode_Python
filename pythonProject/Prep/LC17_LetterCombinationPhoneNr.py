from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        self.letter_digit_mapping = {
            "2": ["a", "b", "c"],
            "3": ["d", "e", "f"],
            "4": ["g", "h", "i"],
            "5": ["j", "k", "l"],
            "6": ["m", "n", "o"],
            "7": ["p", "q", "r", "s"],
            "8": ["t", "u", "v"],
            "9": ["w", "x", "y", "z"],
        }
        if not digits:
            return []
        self.res = []
        self.backtrack(digits,0,[])
        return self.res

    def backtrack(self, digits, cur_idx, cur_res):
        if cur_idx >= len(digits):
            self.res.append("".join(cur_res))

            return
        else:
            for char in self.letter_digit_mapping[digits[cur_idx]]:
                cur_res.append(char)
                self.backtrack(digits, cur_idx + 1, cur_res)
                cur_res.pop()
