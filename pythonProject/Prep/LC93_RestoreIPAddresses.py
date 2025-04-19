from typing import List


class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        """decide where to put dots"""
        res = []
        if len(s) > 12:
            return res

        def backtrack(i, dots, curIP):
            """

            :param i: index we are at
            :param dots: how many inserted so far
            :param curIP: what do we build
            :return:
            """
            if dots == 4 and i == len(s):
                # it has 4th dote in a string, so it should be deleted
                res.append(curIP[:-1])
                return
            if dots > 4:
                return
            # start from i, where we are at and then dont go out of string
            for j in range(i, min(i + 3, len(s))):
                # last is not included, no leading zeros
                if int(s[i:j + 1]) < 256 and (i == j or s[i] != "0"):
                    backtrack(j + 1, dots + 1, curIP + s[i:j + 1] + ".")

        backtrack(0, 0, "")
        return res


if __name__ == "__main__":
    s = "25525511135"
    print(Solution().restoreIpAddresses(s))
