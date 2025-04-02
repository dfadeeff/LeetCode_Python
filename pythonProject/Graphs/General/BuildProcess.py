from collections import defaultdict, deque
from typing import List


class Solution:
    def killProcess(self, pid: List[int], ppid: List[int], kill: int) -> List[int]:
        tree = defaultdict(list)
        for child, parent in zip(pid, ppid):
            tree[parent].append(child)
        print(tree)
        result = []
        queue = deque([kill])

        while queue:
            current = queue.popleft()
            result.append(current)
            for child in tree[current]:
                queue.append(child)

        return result


if __name__ == '__main__':
    pid = [1, 3, 10, 5]
    ppid = [3, 0, 5, 3]
    kill = 5
    print(Solution().killProcess(pid, ppid, kill))
    pid = [1, 2, 3]
    ppid = [0, 1, 2]
    kill = 1
    print(Solution().killProcess(pid, ppid, kill))
