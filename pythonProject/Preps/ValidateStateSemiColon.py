from typing import List


class Solution:

    def validateStack(self, logs: List[str]):
        stack = []
        for log in logs:
            func, action = log.split(":")
            print("func: ", func, " action: ", action)
            if action == "start":
                stack.append(func)
            elif action == "end":
                if not stack or stack[-1] != func:
                    return False
                stack.pop()
        return not stack


if __name__ == "__main__":
    input = ["funcA:start", "funcB:start", "funcB:end", "funcA:end"]
    print(Solution().validateStack(input))
