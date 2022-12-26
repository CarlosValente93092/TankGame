class Tank:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.health = 100
        self.pos = pos

    def move(self, direction: tuple[int, int]) -> None:
        self.pos = tuple([self.pos[i] + direction[i] for i in range(2)])
