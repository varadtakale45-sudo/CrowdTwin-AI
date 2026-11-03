import heapq


class LinkedList:
    class Node:
        def __init__(self, value): self.value, self.next = value, None
    def __init__(self): self.head = self.tail = None
    def append(self, value):
        node = self.Node(value)
        if self.tail: self.tail.next = node
        else: self.head = node
        self.tail = node
    def values(self):
        out, node = [], self.head
        while node: out.append(node.value); node = node.next
        return out


class DoublyLinkedList:
    class Node:
        def __init__(self, value): self.value, self.prev, self.next = value, None, None
    def __init__(self): self.head = self.tail = None
    def append(self, value):
        n = self.Node(value); n.prev = self.tail
        if self.tail: self.tail.next = n
        else: self.head = n
        self.tail = n


class CircularLinkedList(LinkedList):
    def append(self, value):
        super().append(value); self.tail.next = self.head


class Stack:
    def __init__(self): self._items = []
    def push(self, item): self._items.append(item)
    def pop(self): return self._items.pop() if self._items else None


class Queue:
    def __init__(self): self._items = []
    def enqueue(self, item): self._items.append(item)
    def dequeue(self): return self._items.pop(0) if self._items else None


class CircularQueue:
    def __init__(self, size): self.data, self.size, self.index = [None] * size, size, 0
    def enqueue(self, item): self.data[self.index] = item; self.index = (self.index + 1) % self.size


class PriorityQueue:
    def __init__(self): self.heap = []
    def put(self, priority, item): heapq.heappush(self.heap, (priority, item))
    def get(self): return heapq.heappop(self.heap) if self.heap else None


def occupancy_grid(nodes, size=10):
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for n in nodes:
        grid[int((n["x"] + 20) / 40 * (size-1))][int((n["z"] + 15) / 30 * (size-1))] += n["crowd"]
    return grid


def congestion_heap(nodes):
    heap = [(-n["density"], n["id"]) for n in nodes]; heapq.heapify(heap); return heap

