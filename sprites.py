# Standard library imports
import pygame

# Local imports
from bullet import Bullet
from tank import Tank
from terrain import Terrain
from typing import Tuple


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, SCALE) -> None:
        super().__init__()

        # Scale of the sprite
        self.scale: int = SCALE
        # Create a surface to draw on
        self.image: pygame.Surface = pygame.Surface([self.scale, self.scale])
        # Set the colorkey for the surface, which will be transparent when drawn
        self.image.set_colorkey("white")
        # Create a rect based on the surface
        self.rect: pygame.Rect = self.image.get_rect()


class BulletSprite(BaseSprite):
    def __init__(self, bullet: Bullet, SCALE) -> None:
        super().__init__(SCALE)

        # The bullet object associated with this sprite
        self.bullet: Bullet = bullet
        # Load the image for the bullet
        self.image: pygame.Surface = pygame.image.load("images/bullet.png").convert()
        # Set the colorkey for the image, which will be transparent when drawn
        self.image.set_colorkey(self.image.get_at((0, 0)))
        # Create a rect based on the image
        self.rect: pygame.Rect = self.image.get_rect()
        # Set the top left position of the rect to the position of the bullet
        self.rect.topleft: Tuple[int, int] = self.bullet.pos

    def update(self) -> None:
        # Update the rect position to the position of the bullet
        self.rect.topleft = self.bullet.pos


class TankSprite(BaseSprite):
    def __init__(self, tank: Tank, SCALE) -> None:
        '''Initialize TankSprite object'''
        # Call superclass initialization method
        super().__init__(SCALE)

        # Set attribute "tank" to the passed Tank object
        self.tank: Tank = tank
        # Load image for sprite and set its colorkey to the color of the top left pixel
        self.image: pygame.Surface = pygame.image.load("images/tank.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        # Get a rectangular area that encloses the sprite image
        self.rect: pygame.Rect = self.image.get_rect()
        # Set the top left corner of the rectangular area to the position of the Tank object
        self.rect.topleft: Tuple[int, int] = self.tank.pos
        # WANT 43x21, HAVE 71x37
        new_width, new_height = 43, 21
        self.rect = self.rect.move(new_width - self.rect.width, new_height - self.rect.height)
        # Set the center position of the Tank object to the center of the rectangular area
        self.tank.set_center_pos(self.rect.center)
        # Set the position of the bullet in the Tank object to the center position of the Tank object
        self.tank.bullet.set_pos(self.tank.center_pos)

    def update(self) -> None:
        '''Update sprite's position and Tank object's center position'''
        # Set the top left corner of the rectangular area to the position of the Tank object
        self.rect.topleft = self.tank.pos
        # Set the center position of the Tank object to the center of the rectangular area
        self.tank.set_center_pos(self.rect.center)

    def get_bottom_pos(self) -> int:
        '''Return the y-coordinate of the bottom of the sprite'''
        return self.tank.pos[1]+self.image.get_height()


class TerrainSprite(BaseSprite):
    def __init__(self, terrain: Terrain, SCALE) -> None:
        '''Initialize TerrainSprite object'''
        super().__init__(SCALE)

        # Assign terrain object to sprite
        self.terrain: Terrain = terrain
        # Scale the image based on the terrain width and height
        self.image: pygame.Surface = pygame.transform.scale(self.image, (self.terrain.width, self.terrain.height))
        # Get the rect of the image and move the rect to the y position of the terrain
        self.rect: pygame.Rect = self.image.get_rect().move((0, self.terrain.ypos))
        # Fill the image with the terrain color
        self.image.fill(self.terrain.color)
