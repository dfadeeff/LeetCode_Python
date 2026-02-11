class Animal:
    pass


class Wolf(Animal):
    def __init__(self, legs):
        self.legs = legs

    def _roar(self):
        print("I'm roaring and have", self.legs, "legs")


if __name__ == "__main__":
    w1 = Wolf(4)
    w1._roar()
    w2 = Wolf(6)
    w2._roar()
