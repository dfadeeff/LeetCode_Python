class Solution:
    def maximum69Number(self, num: int) -> int:
        # change simply left most digit 6 to 9
        array = [int(digit) for digit in str(num)]

        for i in range(len(array)):
            if array[i] == 6:
                array[i] = 9
                break

        return int(''.join(map(str,array)))


def main():
    num = 9669
    print(Solution().maximum69Number(num))
    num = 9996
    print(Solution().maximum69Number(num))


if __name__ == '__main__':
    main()
