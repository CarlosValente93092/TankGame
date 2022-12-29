# Standard library imports
import math

# Local imports
from bullet import Bullet
import input_handler
import fsm


class Tank:
    def __init__(self, pos: tuple[int, int], controls) -> None:
        # Set the health of the tank to a static 100
        self.health: int = 100
        # Set tank's position
        self.pos = pos
        # Create a bullet entity for tank
        self.bullet = Bullet(self.pos)
        # Define angle to shoot the bullet
        self.bullet_angle = -math.pi/4
        # Define power to shoot the bullet
        self.bullet_power = 50
        # Define FSM for each tank
        self.fsm = fsm.FSM(fsm.STATES, fsm.TRANSITIONS)
        # Define input handler for tank
        self.IH = input_handler.InputHandler()
        # Define tank controls (1-qweasd or 2-uiojkl)
        self.controls = controls
        # Define tank turn to play
        self.current_player = False
        # Define when bullet hitted something to pass to next tank turn
        self.bulletHit = False

    def get_controls(self):
        return self.IH.get_controls_1() if self.controls == 1 else self.IH.get_controls_2()

    def move(self, direction: tuple[int, int]) -> None:
        '''Updates tanks position accordingly'''
        self.pos = tuple([self.pos[i] + direction[i] for i in range(2)])
        self.bullet.set_pos(self.center_pos)

    def shoot(self) -> None:
        '''Calls bullet's shoot function with correct parameters'''
        self.bullet.shoot(self.center_pos, self.bullet_angle, self.bullet_power)

    def update(self, events):
        '''Updates tank actions'''
        self.commands = self.IH.update(events)
        event = None

        if self.bulletHit:  # Bullet finished it's air time and switch to next player
            event = fsm.Event.IDLE
        else:
            if self.current_player:
                event = fsm.Event.MOVING
            if any(isinstance(cmd(), input_handler.SHOOT) for cmd in self.commands.values()):
                event = fsm.Event.FIRING
            if self.bullet.shooting:
                event = fsm.Event.RELOADING
        # event = fsm.Event.DESTROYED

        self.fsm.update(event=event, object=self)

    def set_center_pos(self, pos):
        self.center_pos = pos

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
