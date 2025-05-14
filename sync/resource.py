class Resource:
    def __init__(self, name, count):
        self.name = name
        self.count = count
        self.available = count
        self.queue = []

    def __repr__(self):
        return f"<{self.name}: {self.available}/{self.count}>"
