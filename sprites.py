# Third-party imports
import pygame

# Local imports
from bullet import Bullet
from tank import Tank
from terrain import Terrain


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, SCALE) -> None:
        super().__init__()

        self.scale = SCALE
        self.image = pygame.Surface([self.scale, self.scale])
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()


class BulletSprite(BaseSprite):
    def __init__(self, bullet: Bullet, SCALE) -> None:
        super().__init__(SCALE)

        self.bullet = bullet
        self.image = pygame.image.load("images/bullet.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()  # gets rect from surface
        self.rect.topleft = self.bullet.pos

    def update(self):
        self.rect.topleft = self.bullet.pos


class TankSprite(BaseSprite):
    def __init__(self, tank: Tank, SCALE) -> None:
        super().__init__(SCALE)

        self.tank = tank
        self.image = pygame.image.load("images/tank.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()  # gets rect from surface
        self.rect.topleft = self.tank.pos
        self.tank.set_center_pos(self.rect.center)
        self.tank.bullet.set_pos(self.tank.center_pos)

    def update(self):
        self.rect.topleft = self.tank.pos
        self.tank.set_center_pos(self.rect.center)

    def get_bottom_pos(self):
        return self.tank.pos[1]+self.image.get_height()


class TerrainSprite(BaseSprite):
    def __init__(self, terrain: Terrain, SCALE) -> None:
        super().__init__(SCALE)

        self.terrain = terrain
        self.image = pygame.transform.scale(self.image, (self.terrain.width, self.terrain.height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((0, self.terrain.ypos))
        self.image.fill(self.terrain.color)
