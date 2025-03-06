class Solution:
    def confusingNumber(self, n: int) -> bool:
        rotate_map = {'0': '0', '1': '1', '6': '9', '8': '8', '9': '6'}
        n_str = str(n)

        rotated_str = ''
        for digit in reversed(n_str):  # 🔹 Reverse while rotating
            if digit not in rotate_map:
                return False  # 🔹 Invalid digit found, return False immediately
            rotated_str += rotate_map[digit]

        return int(rotated_str) != n  # 🔹 Compare rotated number with original




if __name__ == '__main__':
    n = 89
    print(Solution().confusingNumber(n))
    n = 11
    print(Solution().confusingNumber(n))
    n = 916
    print(Solution().confusingNumber(n))
