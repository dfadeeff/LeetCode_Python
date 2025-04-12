class Solution:
    def maximumSwap(self, num: int) -> int:
        num_str = list(str(num))
        print(num_str)
        last_index = {int(d): i for i, d in enumerate(num_str)}
        print(last_index)

        for i, digit in enumerate(num_str):
            for d in range(9,int(digit),-1):
                if d in last_index and last_index[d] > i:
                    num_str[i], num_str[last_index[d]] = num_str[last_index[d]], num_str[i]
                    return int("".join(num_str))

        return num


if __name__ == '__main__':
    num = 2736
    print(Solution().maximumSwap(num))
    num = 9973
    print(Solution().maximumSwap(num))

