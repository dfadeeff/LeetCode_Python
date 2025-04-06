"""
The read4 API is already defined for you.

    @param buf4, a list of characters
    @return an integer
    def read4(buf4):

# Below is an example of how the read4 API can be called.
file = File("abcdefghijk") # File is "abcdefghijk", initially file pointer (fp) points to 'a'
buf4 = [' '] * 4 # Create buffer with enough space to store characters
read4(buf4) # read4 returns 4. Now buf = ['a','b','c','d'], fp points to 'e'
read4(buf4) # read4 returns 4. Now buf = ['e','f','g','h'], fp points to 'i'
read4(buf4) # read4 returns 3. Now buf = ['i','j','k',...], fp points to end of file
"""
from typing import List


class File:
    def __init__(self, content):
        self.content = content
        self.pointer = 0

    def read4(self, buf4):
        count = 0
        while count < 4 and self.pointer < len(self.content):
            buf4[count] = self.content[self.pointer]
            self.pointer += 1
            count += 1
        return count


class Solution:

    def __init__(self, file):
        self.file = file
        # internal buffer to hold extra read4 chars
        self.buf4 = [""] * 4
        self.buf4_ptr = 0  # pointer in buf4
        self.buf4_size = 0  # number of valid chars in buf4

    def read(self, buf: List[str], n: int) -> int:
        """
        •	✅ Reads at most 4 characters from file
        •	✅ Copies them into buf4
        •	✅ Advances file pointer
        •	✅ Returns how many chars were actually read
	    """
        copied_chars = 0  # how many chars copied to output buffer

        while copied_chars < n:
            # Step 1: if internal buffer is empty, refill
            if self.buf4_ptr == self.buf4_size:
                self.buf4_size = self.file.read4(self.buf4)
                self.buf4_ptr = 0
                if self.buf4_size == 0:  # EOF
                    break

            # Step 2: copy from internal buffer to output buffer
            while copied_chars < n and self.buf4_ptr < self.buf4_size:
                buf[copied_chars] = self.buf4[self.buf4_ptr]
                copied_chars += 1
                self.buf4_ptr += 1

        return copied_chars


if __name__ == '__main__':
    file = File("abcdefghijk")
    solution = Solution(file)

    buf1 = [""] * 4
    print(solution.read(buf1, 4), "".join(buf1[:4]))  # 4 abcd

    buf2 = [""] * 4
    print(solution.read(buf2, 4), "".join(buf2[:4]))  # 4 efgh

    buf3 = [""] * 4
    print(solution.read(buf3, 4), "".join(buf3[:3]))  # 3 ijk
