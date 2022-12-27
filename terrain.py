class Terrain:
    def __init__(self, WIDTH, HEIGHT, SCALE, color, ypos) -> None:
        self.friction = 1
        self.width = WIDTH*SCALE
        self.height = HEIGHT*SCALE - ypos
        self.color = color
        self.ypos = ypos
