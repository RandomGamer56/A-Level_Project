class ThreadReturn:
    def __init__(self):
        self.item = []

    def size(self):
        return len(self.item)

    def isEmpty(self):
        if self.size() == 0:
            return True
        else:
            return False

    def enque(self, item):
        self.item.append(item)
        return True

    def deque(self):
        if self.size() == 0:
            return None
        else:
            return self.item.pop()

def handler():
    return ThreadReturn()
