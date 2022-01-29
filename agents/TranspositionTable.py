class Position:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None

class TranspositionTable:
    def __init__(self):
        self.prehead = Position(None,None)

    def search(self, key):
        p = self. prehead.next
        while p:
            if p.key == key:
              return p
            p = p.next
        return None

    def add(self, key, value):
        p = self.search(key)
        if p:
            p.val= value
        else:
            position = Position(key, value)
            self.prehead.next, position.next = position, self.prehead.next

    def get(self, key):
        p = self.search(key)
        if p:
            return p.val
        else:
            return None

    def serialize(self):
        p = self.prehead.next
        ret = []
        while p:
            ret.append([p.key, p.val])
            p = p.next
        return ret

class MyHashMap:
   def __init__(self):
      self.size = 1033
      self.arr = [TranspositionTable() for _ in range(self.size)]
   def _hash(self, key):
      return key % self.size
   def put(self, key, value):
      h = self._hash(key)
      self.arr[h].add(key, value)
   def get(self, key):
      h = self._hash(key)
      ret = self.arr[h].get(key)
      if ret is not None:
         return ret
      else:
         return -1
   def remove(self, key):
      h = self._hash(key)
      self.arr[h].remove(key)