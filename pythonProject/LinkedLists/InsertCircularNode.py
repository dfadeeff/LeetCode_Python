class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


class Solution:
    def insert(self, head: 'Optional[Node]', insertVal: int) -> 'Node':
        new_node = Node(insertVal)

        if not head:
            new_node.next = new_node  # Point to itself
            return new_node

        curr = head
        while True:
            # Normal case: insertVal fits between curr and curr.next
            if curr.val <= insertVal <= curr.next.val:
                break

            # Wrap-around case: curr > curr.next (end of sorted list)
            if curr.val > curr.next.val:
                if insertVal >= curr.val or insertVal <= curr.next.val:
                    break

            curr = curr.next

            # Full loop done — all nodes are same or no perfect fit
            if curr == head:
                break

        # Insert new_node between curr and curr.next
        new_node.next = curr.next
        curr.next = new_node

        return head


if __name__ == '__main__':
    head = Node(3)
    head.next = Node(4)
    head.next.next = Node(1)
    head.next.next.next = head
    insertVal = 2
    result = Solution().insert(head, insertVal)

    # Print the modified linked list
    # Print the modified circular linked list once
    curr = result
    start = result
    output = []
    while True:
        output.append(str(curr.val))
        curr = curr.next
        if curr == start:
            break

    print(" -> ".join(output) + " -> ... (circular)")
