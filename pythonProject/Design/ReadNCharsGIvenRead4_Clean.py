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

    def read(self, buf, n):
        """

        Single call read, with internal buffer

        :type buf: Destination buffer (List[str])
        :type n: Number of characters to read (int)
        :rtype: The number of actual characters read (int)

        For a follow up

        “I maintain an internal buffer and pointer to cache the extra characters from read4(). Before calling read4(), I always check my internal buffer first.

        Interviewer will love if you say:

“Since I have only read4(), I will manage an internal buffer to cache extra characters. On each call to read(), I will copy from the internal buffer first before calling read4(). This lets me handle multiple read calls efficiently, and it avoids reading from the file system unnecessarily.”


        """
        buf4 = [''] * 4  # Temporary buffer
        total_read = 0

        while total_read < n:
            chars_read = self.file.read4(buf4)  # Read up to 4 chars
            if chars_read == 0:
                break  # End of file

            # Determine how many characters to copy (may not need all 4)
            chars_to_copy = min(chars_read, n - total_read)

            # Copy from buf4 to buf
            for i in range(chars_to_copy):
                buf.append(buf4[i])

            total_read += chars_to_copy

        return total_read

if __name__ == '__main__':
    file = File("abcdefghijk")
    solution = Solution(file)

    buf = [""] * 10
    num_read = solution.read(buf, 7)
    print("Characters read:", num_read)
    print("Buffer:", "".join(buf[:num_read]))