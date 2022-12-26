import math


class Bullet:
    def __init__(self, pos) -> None:
        # Set the acceleration due to gravity
        self.gravity: float = 9.81 * 10
        # Set the initial x and y position of the bullet
        self.pos = pos
        # Set the time step (how often the bullet position is updated)
        self.time_step = 0.05
        # Set the initial time
        self.time = 0
        # Set flag to identify bullet is moving or stopped
        self.shooting = False

    def shoot(self, pos, angle, power) -> None:
        '''Function to reset bullets parameters to be ready to be shot'''
        # Redefine bullet to position to tank's position
        self.pos = pos
        # Bullet is now on the move
        self.shooting = True
        # Reset time bullet is on air
        self.time = 0
        # Set bullet angle
        self.angle = angle
        # Set bullet power
        self.power = power
        # Set initial velocity
        self.velocity = (power * math.cos(angle), power * math.sin(angle))

    def update(self):
        '''Updates the bullets position according to angle, power and gravity while bullet is on air'''
        if (self.shooting):
            # Update the x and y position of the bullet
            self.pos = (self.pos[0] + self.velocity[0] * self.time + 0.5 * 0 * self.time**2,
                        self.pos[1] + self.velocity[1] * self.time + 0.5 * self.gravity * self.time**2)

            # Increase the time
            self.time += self.time_step
