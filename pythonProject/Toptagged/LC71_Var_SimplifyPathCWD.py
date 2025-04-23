from typing import List


class Solution:
    def changeDirectory(self, cwd: str, cd: str):
        if not cd:
            return cwd or "/"

        # Determine the starting point: root for absolute paths, cwd tokens for relative
        if cd.startswith("/"):
            tokens: List[str] = []
        else:
            tokens = [t for t in cwd.split("/") if t]

        # Process each segment in cd
        for segment in cd.split("/"):
            if segment == "" or segment == ".":
                # Skip empty segments (due to "//") and current‐dir markers
                continue
            if segment == "..":
                # Go up one directory if possible
                if tokens:
                    tokens.pop()

            else:
                # Regular directory name: descend into it
                tokens.append(segment)
        # Reconstruct the simplified path
        return "/" + "/".join(tokens) if tokens else "/"


if __name__ == "__main__":
    cwd = "/a/b/c"
    cd = "/d/./e"
    print(Solution().changeDirectory(cwd, cd))
