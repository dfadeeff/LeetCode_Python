from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        mapping = {
            '2': "abc",
            '3': "def",
            '4': "ghi",
            '5': "jkl",
            '6': "mno",
            '7': "pqrs",
            '8': "tuv",
            '9': "wxyz"
        }
        results = []

        def backtrack(index, current_combination):
            # If our current combination has length == length of digits, we've formed a full combination
            if len(current_combination) == len(digits):
                results.append("".join(current_combination))
                return

            # Identify which digit we are working with
            current_digit = digits[index]
            print("current digit", current_digit)
            # Retrieve all possible letters for this digit
            possible_letters = mapping[current_digit]
            print("possible letters", possible_letters)

            # Try each letter and recurse
            for letter in possible_letters:
                current_combination.append(letter)
                # Move to the next digit in the input! once the length is equal to the input, we stop, see above
                backtrack(index + 1, current_combination)
                # Backtrack step: remove the letter before trying the next one, come back to the previous decision point
                current_combination.pop()

        backtrack(0, [])
        return results


def main():
    digits = "23"
    print(Solution().letterCombinations(digits))
    digits = ""
    print(Solution().letterCombinations(digits))


if __name__ == '__main__':
    main()
