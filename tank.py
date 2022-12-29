# Standard library imports
import math
from typing import List, Tuple, Dict, Type

# Local imports
from bullet import Bullet
from input_handler import InputHandler, SHOOT, Command
from fsm import FSM, STATES, TRANSITIONS, Event


class Tank:
    def __init__(self, pos: Tuple[int, int], controls: int) -> None:
        # Set the static health of the tank to 100
        self.health: int = 100
        # Set the position of the tank
        self.pos: Tuple[int, int] = pos
        # Create a bullet entity for the tank
        self.bullet: Bullet = Bullet(self.pos)
        # Set the initial angle to shoot the bullet
        self.bullet_angle: float = -math.pi/4
        # Set the initial power to shoot the bullet
        self.bullet_power: int = 50
        # Create a finite state machine for the tank
        self.fsm: FSM = FSM(STATES, TRANSITIONS)
        # Create an input handler for the tank
        self.IH: InputHandler = InputHandler()
        # Set the controls for the tank (1 for qweasd or 2 for uiojkl)
        self.controls: int = controls
        # Set the flag for the current player to False
        self.current_player: bool = False
        # Set the flag for when the bullet has hit something to False
        self.bulletHit: bool = False

    def get_controls(self) -> List[int]:
        '''Returns the controls for the current player'''
        # Return controls for player 1 if self.controls is 1, otherwise return controls for player 2
        return self.IH.get_controls_1() if self.controls == 1 else self.IH.get_controls_2()

    def move(self, direction: Tuple[int, int]) -> None:
        '''Updates tanks position accordingly'''
        # Update the position of the tank
        self.pos = tuple(a + b for a, b in zip(self.pos, direction))
        # Update the position of the bullet
        self.bullet.set_pos(self.center_pos)

    def shoot(self) -> None:
        '''Calls bullet's shoot function with correct parameters'''
        # Call the shoot method of the bullet, passing the center position, angle, and power of the bullet
        self.bullet.shoot(self.center_pos, self.bullet_angle, self.bullet_power)

    def update(self, events) -> None:
        '''Updates tank actions'''
        # Get input commands inserted by the player
        self.commands: Dict[int, Type[Command]] = self.IH.update(events)
        event = None

        # Check the current state of the tank
        # Bullet finished its air time and switch to next player
        if self.bulletHit:
            # Set the event to IDLE
            event = Event.IDLE
        # If tanks healths drops to zero or below means is was destroyed
        elif self.health <= 0:
            # Set the event to DESTROYED
            event = Event.DESTROYED
        else:
            # Tank can move if it is in it's turn
            if self.current_player:
                # Set the event to MOVING
                event = Event.MOVING
            # Tanks is now ready to shoot
            if any(isinstance(cmd(), SHOOT) for cmd in self.commands.values()):
                # Set the event to FIRING
                event = Event.FIRING
            # Bullet is on air ready to hit a target
            if self.bullet.shooting:
                # Set the event to RELOADING
                event = Event.RELOADING

        # Update the state machine
        return self.fsm.update(event=event, object=self)

    def set_center_pos(self, pos: Tuple[int, int]) -> None:
        '''Sets the center position of the tank'''
        # Set the center position of the tank
        self.center_pos: Tuple[int, int] = pos

    def set_angle(self, angle: float) -> None:
        '''Changes bullet angle'''
        # Update the bullet angle
        self.bullet_angle += angle
        # Clamp the bullet angle to the range -pi to 0
        if self.bullet_angle > 0:
            self.bullet_angle = 0
        elif self.bullet_angle < -math.pi:
            self.bullet_angle = -math.pi

    def set_power(self, power: float) -> None:
        '''Changes bullet power'''
        # Update the bullet power
        self.bullet_power += power
        # Clamp the bullet power to the range 0-100
        if self.bullet_power > 100:
            self.bullet_power = 100
        elif self.bullet_power < 0:
            self.bullet_power = 0
