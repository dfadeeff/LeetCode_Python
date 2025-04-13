from typing import Optional, List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """merge two at a time, in pairs, so run time is log K since we have K lists
        Takes O(N) to merge so it will be N log K
        """
        if not lists:
            return None
        # pairwise, starts at 1
        interval = 1
        while interval < len(lists):
            # step is 2, so cut in half
            for i in range(0, len(lists) - interval, interval*2):
                lists[i] = self.merge(lists[i], lists[i + interval])

            interval *= 2
        return lists[0]

    def merge(self, l1, l2):
        if not l1:
            return l2
        elif not l2:
            return l1
        else:
            if l1.val <= l2.val:
                l1.next = self.merge(l1.next, l2)
                return l1
            else:
                l2.next = self.merge(l1, l2.next)
                return l2




if __name__ == '__main__':
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    print(Solution().mergeKLists(lists))
