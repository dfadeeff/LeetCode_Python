class FreqStack:

    def __init__(self):
        self.cnt = {}
        self.maxCnt = 0
        self.stacks = {}

    def push(self, val: int) -> None:
        valCnt = 1 + self.cnt.get(val, 0)
        self.cnt[val] = valCnt

        if valCnt > self.maxCnt:
            self.maxCnt = valCnt
            self.stacks[valCnt] = []

        self.stacks[valCnt].append(val)

    def pop(self) -> int:
        res = self.stacks[self.maxCnt].pop()
        self.cnt[res] -= 1
        if not self.stacks[self.maxCnt]:

            self.maxCnt -= 1
        return res

if __name__ == "__main__":
    obj = FreqStack()
    print(obj.push(5))
    print(obj.push(7))
    print(obj.push(5))
    print(obj.push(7))
    print(obj.push(4))
    print(obj.push(5))
    print(obj.pop())
    print(obj.pop())
    print(obj.pop())
    print(obj.pop())

