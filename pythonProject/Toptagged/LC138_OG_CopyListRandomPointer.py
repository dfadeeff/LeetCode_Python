class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        oldCopy = {None: None}
        cur = head
        while cur:
            copy = Node(cur.val)
            oldCopy[cur] = copy
            cur = cur.next

        cur = head
        while cur:
            copy = oldCopy[cur]
            copy.next = oldCopy[cur.next]
            copy.random = oldCopy[cur.random]
            cur = cur.next
        return oldCopy[head]


if __name__ == "__main__":
    # Build head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
    nodes = [Node(7) for _ in range(5)]
    nodes[1] = Node(13)
    nodes[2] = Node(11)
    nodes[3] = Node(10)
    nodes[4] = Node(1)
    # link next pointers
    for i in range(4):
        nodes[i].next = nodes[i + 1]
    # link random pointers by index
    # index 0 → random = None
    nodes[0].random = None
    # index 1 → random = 0
    nodes[1].random = nodes[0]
    # index 2 → random = 4
    nodes[2].random = nodes[4]
    # index 3 → random = 2
    nodes[3].random = nodes[2]
    # index 4 → random = 0
    nodes[4].random = nodes[0]

    head = nodes[0]
    copy = Solution().copyRandomList(head)

    # walk both lists and print val and random.val
    orig, cpy = head, copy
    print("orig\t-> copy")
    while orig:
        o_rnd = orig.random.val if orig.random else None
        c_rnd = cpy.random.val if cpy.random else None
        print(f"{orig.val} (r:{o_rnd})\t   {cpy.val} (r:{c_rnd})")
        orig, cpy = orig.next, cpy.next
