class BST:
    def __init__(self): self.root = None
    def insert(self, key, value): self.root = self._insert(self.root, key, value)
    def _insert(self, node, key, value):
        if not node: return [key, value, None, None, 1]
        side = 2 if key < node[0] else 3; node[side] = self._insert(node[side], key, value); return node
    def inorder(self):
        out = []
        def walk(n):
            if n: walk(n[2]); out.append((n[0], n[1])); walk(n[3])
        walk(self.root); return out


class AVLTree(BST):
    def _height(self, n): return n[4] if n else 0
    def _insert(self, n, key, value):
        if not n: return [key, value, None, None, 1]
        side = 2 if key < n[0] else 3; n[side] = self._insert(n[side], key, value)
        n[4] = 1 + max(self._height(n[2]), self._height(n[3])); balance = self._height(n[2]) - self._height(n[3])
        if balance > 1:
            if key > n[2][0]: n[2] = self._left(n[2])
            return self._right(n)
        if balance < -1:
            if key < n[3][0]: n[3] = self._right(n[3])
            return self._left(n)
        return n
    def _left(self, x):
        y, t = x[3], x[3][2]; y[2], x[3] = x, t
        x[4] = 1 + max(self._height(x[2]), self._height(x[3])); y[4] = 1 + max(self._height(y[2]), self._height(y[3])); return y
    def _right(self, y):
        x, t = y[2], y[2][3]; x[3], y[2] = y, t
        y[4] = 1 + max(self._height(y[2]), self._height(y[3])); x[4] = 1 + max(self._height(x[2]), self._height(x[3])); return x


class HashTable:
    def __init__(self, size=31): self.buckets = [[] for _ in range(size)]
    def put(self, key, value):
        bucket = self.buckets[hash(key) % len(self.buckets)]
        for pair in bucket:
            if pair[0] == key: pair[1] = value; return
        bucket.append([key, value])
    def get(self, key):
        for k, v in self.buckets[hash(key) % len(self.buckets)]:
            if k == key: return v
        return None

