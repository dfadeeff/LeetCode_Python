# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
from collections import deque


class NestedInteger:
    def __init__(self, value=None):
        if value is None:
            self._list = []
            self._integer = None
        elif isinstance(value, int):
            self._list = None
            self._integer = value
        else:  # if list
            self._list = value
            self._integer = None

    def isInteger(self):
        return self._integer is not None

    def add(self, elem):
        if self._list is None:
            self._list = []
        self._list.append(elem)

    def setInteger(self, value):
        self._integer = value
        self._list = None

    def getInteger(self):
        return self._integer

    def getList(self):
        return self._list


from typing import List


class Solution:
    def depthSum(self, nestedList: List[NestedInteger]) -> int:
        depth = 1
        res = 0
        queue = deque(nestedList)
        print(queue)
        while queue:
            for _ in range(len(queue)):
                curr = queue.popleft()
                print("curr:", curr)
                if curr.isInteger():
                    res += curr.getInteger() * depth
                else:
                    queue.extend(curr.getList())

            depth += 1
        return res

def build_nested_list(data):
    if isinstance(data, int):
        return NestedInteger(data)
    nested = NestedInteger()
    for item in data:
        nested.add(build_nested_list(item))
    return nested


if __name__ == '__main__':
    nestedList = build_nested_list([[1, 1], 2, [1, 1]]).getList()
    print(Solution().depthSum(nestedList))  # Output: 10
