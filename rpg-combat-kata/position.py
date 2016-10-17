
class Position:

    def __init__(self):
        self.position = 0

    def current_position(self):
        return self.position

    def move(self, position):
        self.position = position
