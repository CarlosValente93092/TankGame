import pygame

VALUE_ANGLE_LEFT = -0.05
VALUE_ANGLE_RIGHT = -VALUE_ANGLE_LEFT
VALUE_MOVE_LEFT = (-1, 0)
VALUE_MOVE_RIGHT = (-VALUE_MOVE_LEFT[0], VALUE_MOVE_LEFT[1])
VALUE_POWER_DOWN = -1
VALUE_POWER_UP = -VALUE_POWER_DOWN


class InputHandler:
    def __init__(self) -> None:
        self.commands = {
            pygame.K_q: ANGLE_LEFT,
            pygame.K_w: POWER_UP,
            pygame.K_e: ANGLE_RIGHT,
            pygame.K_a: MOVE_LEFT,
            pygame.K_s: POWER_DOWN,
            pygame.K_d: MOVE_RIGHT,

            pygame.K_u: ANGLE_LEFT,
            pygame.K_i: POWER_UP,
            pygame.K_o: ANGLE_RIGHT,
            pygame.K_j: MOVE_LEFT,
            pygame.K_k: POWER_DOWN,
            pygame.K_l: MOVE_RIGHT,

            pygame.K_SPACE: SHOOT
        }

    def update(self, events):
        '''Returns list of all commands available'''
        return {key: value for key, value in self.commands.items() if events[key]}

    def get_controls_1(self):
        return [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_a, pygame.K_s, pygame.K_d]

    def get_controls_2(self):
        return [pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_j, pygame.K_k, pygame.K_l]


class Command:
    def __init__(self):
        self.actor = None

    def execute(self, actor):
        raise NotImplemented


class ANGLE_LEFT(Command):
    def execute(self, actor):
        self.actor = actor
        actor.set_angle(VALUE_ANGLE_LEFT)


class ANGLE_RIGHT(Command):
    def execute(self, actor):
        self.actor = actor
        actor.set_angle(VALUE_ANGLE_RIGHT)


class POWER_DOWN(Command):
    def execute(self, actor):
        self.actor = actor
        actor.set_power(VALUE_POWER_DOWN)


class POWER_UP(Command):
    def execute(self, actor):
        self.actor = actor
        actor.set_power(VALUE_POWER_UP)


class MOVE_LEFT(Command):
    def execute(self, actor):
        self.actor = actor
        actor.move(VALUE_MOVE_LEFT)


class MOVE_RIGHT(Command):
    def execute(self, actor):
        self.actor = actor
        actor.move(VALUE_MOVE_RIGHT)


class SHOOT(Command):
    def execute(self, actor):
        self.actor = actor
        actor.shoot()
