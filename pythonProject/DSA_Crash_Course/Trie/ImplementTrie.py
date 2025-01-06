class TrieNode:
    def __init__(self):
        self.children = {}  # or a fixed array of size 26 if only 'a'..'z'
        self.endOfWord = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.endOfWord = True

    def search(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.endOfWord

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True


def main():
    trie = Trie()
    print(trie.insert("apple"))
    print(trie.search("apple"))  # return True
    print(trie.search("app"))  # return False
    print(trie.startsWith("app"))  # return True
    print(trie.insert("app"))
    print(trie.search("app"))  # return True


if __name__ == "__main__":
    main()
