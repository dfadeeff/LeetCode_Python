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


class Solution:
    def read(self, buf, n):
        """

        Single call read, without internal buffer

        :type buf: Destination buffer (List[str])
        :type n: Number of characters to read (int)
        :rtype: The number of actual characters read (int)

        For a follow up

        “I maintain an internal buffer and pointer to cache the extra characters from read4(). Before calling read4(), I always check my internal buffer first.

        Interviewer will love if you say:

        “Since I have only read4(), I will manage an internal buffer to cache extra characters. On each call to read(), I will copy from the internal buffer first before calling read4(). This lets me handle multiple read calls efficiently, and it avoids reading from the file system unnecessarily.”


        """
        copiedChars = 0
        readChars = 4
        remainingChars = n

        # While there are at least 4 characters remaining to be read and the last
        # call to readChars returned 4 characters, write directly to buf.
        while remainingChars >= 4 and readChars == 4:
            buf4 = [""] * 4
            # readChars = read4(buf4)
            for i in range(readChars):
                buf[copiedChars + i] = buf4[i]
            copiedChars += readChars

        # If there are between 1 and 3 characters that we still want to read and
        # readChars was not 0 last time we called read4, then create a buffer
        # for just this one call so we can ensure buf does not overflow.
        if remainingChars > 0 and readChars != 0:
            buf4 = [""] * 4
            # readChars = read4(buf4)

            for i in range(min(remainingChars, readChars)):
                buf[copiedChars + i] = buf4[i]
            copiedChars += readChars

        return min(n, copiedChars)
