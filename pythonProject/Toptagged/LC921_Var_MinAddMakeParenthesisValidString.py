from typing import List


class Solution:
    def minimumAddToMakeValid(self, s: str) -> str:
        res: List[str] = []
        balance = 0  # number of unmatched '(' we’ve seen so far

        for c in s:
            if c == '(':
                balance += 1
                res.append(c)

            elif c == ')':
                if balance > 0:
                    # we have a matching '(' in flight
                    balance -= 1
                    res.append(c)
                else:
                    # no '(' to match this ')': insert one
                    res.append('(')
                    res.append(')')
            else:
                # any other character, just carry through
                res.append(c)

        # close off all the opens that never got a ')'
        if balance:
            res.extend(')' * balance)

        return ''.join(res)


if __name__ == "__main__":
    s = "()))"
    print(Solution().minimumAddToMakeValid(s))
