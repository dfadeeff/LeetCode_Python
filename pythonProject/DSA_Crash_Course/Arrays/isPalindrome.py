def isPalindrome(string):
    left = 0;
    right = len(string) - 1;

    while left < right:
        if string[left] != string[right]:
            return False
        left += 1;
        right -= 1;
    return True


if __name__ == '__main__':
    s1 = "arcdfa"
    print(isPalindrome(s1))
    s2 = "alla"
    print(isPalindrome(s2))
