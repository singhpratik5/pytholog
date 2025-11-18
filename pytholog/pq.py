from collections import deque 
from bisect import insort

## the queue object we will use to store goals we need to search
## FIFO (First In First Out)
## using FIFO ensures that if cut is used we have the first answer from the facts fed first to KB
## it is very useful in graph cases to get the shortest path first. But it depends on the order
## the facts were defined in the knowledge base.
class SearchQueue():
    def __init__(self):
        # Use deque as a stack to implement LIFO (depth-first) search
        # Prolog uses depth-first search with backtracking; using LIFO makes
        # the engine explore clause bodies in a Prolog-like order.
        self._container = deque()
    @property
    def empty(self):
        return not self._container
    def push(self, expr):
        self._container.append(expr)
    def pop(self):
        return self._container.pop()  # LIFO pop: depth-first search
    def __repr__(self):
        return repr(self._container)
        
## to store facts and sort them for binary search in queries 
class FactHeap():
    def __init__(self):
        self._container = []

    def push(self, item):
        insort(self._container, item) # in by sort
        
    def __getitem__(self, item):
         return self._container[item]
    
    def __len__(self):
         return len(self._container)
    
    def __repr__(self):
        return repr(self._container)