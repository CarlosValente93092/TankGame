from bullet import Bullet
import math


class Tank:
    def __init__(self, pos: tuple[int, int]) -> None:
        # Set the health of the tank to a static 100
        self.health: int = 100
        # Set tank's position
        self.pos = pos
        # Create a bullet entity for tank
        self.bullet = Bullet(pos)
        # Define angle to shoot the bullet
        self.bullet_angle = -math.pi/4
        # Define power to shoot the bullet
        self.bullet_power = 50

    def move(self, direction: tuple[int, int]) -> None:
        '''Updates tanks position accordingly'''
        self.pos = tuple([self.pos[i] + direction[i] for i in range(2)])

    def shoot(self) -> None:
        '''Calls bullet's shoot function with correct parameters'''
        self.bullet.shoot(self.pos, self.bullet_angle, self.bullet_power)

    def update(self):
        '''Updates bullet position'''
        self.bullet.update()

    def set_angle(self, angle):
        '''Changes bullet angle'''
        self.bullet_angle += angle
        if self.bullet_angle > 0:
            self.bullet_angle = 0
        elif self.bullet_angle < -math.pi:
            self.bullet_angle = -math.pi

    def set_power(self, power):
        '''Changes bullet power'''
        self.bullet_power += power
        if self.bullet_power > 100:
            self.bullet_power = 100
        elif self.bullet_power < 0:
            self.bullet_power = 0
