from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(-1)
        current = dummy
        while list1 and list2:
            if list1.val < list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next  # important to move forward!

        # Attach the remainder
        current.next = list1 if list1 else list2
        return dummy.next


# Convert Python list to linked list
def list_to_linked_list(items):
    dummy = ListNode()
    current = dummy
    for item in items:
        current.next = ListNode(item)
        current = current.next
    return dummy.next


# Convert linked list to Python list
def linked_list_to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


if __name__ == '__main__':
    # Test case
    list1 = [1, 2, 4]
    list2 = [1, 3, 4]

    linked_list1 = list_to_linked_list(list1)
    linked_list2 = list_to_linked_list(list2)
    merged_head = Solution().mergeTwoLists(linked_list1, linked_list2)
    print(linked_list_to_list(merged_head))
