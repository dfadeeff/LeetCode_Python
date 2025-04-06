class Solution:
    def maximumSwap(self, num: int) -> int:
        """Greedy two pass
        To achieve this, we make two passes over the number. In the first pass, we scan from right to left to identify and store the largest digit we find and its position.
        In the second pass, we move from left to right. Now that we know, for each position, the largest digit that appears after it, we check if we can make a swap.
        """
        num_str = list(str(num))
        print("num_str: ", num_str)
        n = len(num_str)
        max_right_index = [0] * n

        max_right_index[n - 1] = n - 1
        for i in range(n - 2, -1, -1):
            max_right_index[i] = (
                i
                if num_str[i] > num_str[max_right_index[i + 1]]
                else max_right_index[i + 1]
            )
        for i in range(n):
            if num_str[i] < num_str[max_right_index[i]]:
                num_str[i], num_str[max_right_index[i]] = (
                    num_str[max_right_index[i]],
                    num_str[i],
                )
                return int("".join(num_str))
        return num


if __name__ == "__main__":
    num = 2736
    print(Solution().maximumSwap(num))
