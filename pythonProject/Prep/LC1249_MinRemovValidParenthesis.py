class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        l_count = r_count = 0
        string_builder = []

        # First pass through the string
        for char in s:
            if char == '(':
                l_count += 1
                # take in the first pass all the time, in a greedy manner
                string_builder.append(char)
            elif char == ')':

                if l_count > r_count:
                    r_count += 1
                    string_builder.append(char)
            else:
                string_builder.append(char)
        # if the counts are equal, done, return string builder
        if l_count == r_count:
            return ''.join(string_builder)
        # otherwise go right to left and remove left parenthesis which took greedily
        else:
            res = []

            # second pass from right to left
            for i in range(len(string_builder) - 1, -1, -1):
                curr = string_builder[i]
                if curr == '(':
                    if l_count <= r_count:
                        res.append(curr)
                    else:
                        l_count -= 1
                elif curr == ')':
                    res.append(curr)
                else:
                    res.append(curr)

        return res[::-1]


if __name__ == '__main__':
    s = "lee(t(c)o)de)"
    print(Solution().minRemoveToMakeValid(s))