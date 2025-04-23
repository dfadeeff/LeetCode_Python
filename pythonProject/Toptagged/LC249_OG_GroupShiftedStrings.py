from collections import defaultdict
from typing import List


class Solution:
    def rotationalCipher(self, s: str, rotation_factor: int):
        """"
        ASCII
        a 97
        A 65
        0 48
        1 49
        2 50
        """


        if rotation_factor == 0:
            return s

        res: List[str] = []
        for ch in s:
            # lowercase
            if 'a' <= ch <= 'z':
                # map ‘a’→0…‘z’→25, add, mod 26, map back
                offset = (ord(ch) - ord('a') + rotation_factor) % 26
                res.append(chr(offset + ord('a')))

            # uppercase
            elif 'A' <= ch <= 'Z':
                offset = (ord(ch) - ord('A') + rotation_factor) % 26
                res.append(chr(offset + ord('A')))

            # digits
            elif '0' <= ch <= '9':
                offset = (ord(ch) - ord('0') + rotation_factor) % 10
                res.append(chr(offset + ord('0')))

            # everything else stays the same
            else:
                res.append(ch)

        return ''.join(res)


if __name__ == "__main__":
    string = "minMerz-894"
    rotational_factor = 5
    print(Solution().rotationalCipher(string, rotational_factor))
