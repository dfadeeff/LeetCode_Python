class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        result = ""
        l_count = 0  # count of unmatched '('
        for char in s:
            if char == '(':
                l_count += 1  # increment opening bracket to balance
                result += "("  # add to the result
            elif char == ')':
                if l_count > 0:
                    l_count -= 1  # decrease l_count because we used one '(' to match.
                    result += ")"
                else:
                    # Add missing '(' before ')'
                    result = '(' + result + ')'
            else:
                # If there are other characters (optional)
                result += char
        # At the end, close any unmatched '('
        result += ')' * l_count

        return result


if __name__ == '__main__':
    s = "())"
    print(Solution().minAddToMakeValid(s))
    s = "((("
    print(Solution().minAddToMakeValid(s))
