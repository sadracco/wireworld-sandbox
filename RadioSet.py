class RadioSet:
    def __init__(self):
        self.buttons = []

    def add(self, b):
        self.buttons.append(b)

    def resetButtons(self):
        for b in self.buttons:
            b.reset()
