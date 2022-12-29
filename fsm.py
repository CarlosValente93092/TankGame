from enum import Enum


class State:
    def __init__(self, name) -> None:
        self.name = name


class Transition:
    def __init__(self, _from, _to) -> None:
        self._from = _from
        self._to = _to


class FSM:
    def __init__(self, states: list[State], transitions: dict[Transition]) -> None:
        self._states = states
        self._transitions = transitions

        self.current: State = self._states[0]
        self.end: State = self._states[-1]

    def update(self, event, object):
        if event:
            for trans in self._transitions.get(event):
                if trans._from == self.current:
                    self.current = trans._to
        self.current.update(object)

        if self.current == self.end:
            return False
        return True


class Event(Enum):
    IDLE = 1,
    MOVING = 2,
    FIRING = 3,
    RELOADING = 4
    DESTROYED = 5


class Idle(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    @classmethod
    def update(self, tank):
        tank.bulletHit = 0
        tank.bullet.set_pos(tank.center_pos)
        tank.bullet.shooting = False
        tank.current_player = False


class Moving(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    @classmethod
    def update(self, tank):
        for key, value in tank.commands.items():
            if key in tank.get_controls():
                value().execute(tank)


class Firing(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    @classmethod
    def update(self, tank):
        tank.shoot()


class Reloading(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    @classmethod
    def update(self, tank):
        tank.bullet.update()


class Destroyed(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    @classmethod
    def update(self, tank):
        pass


STATES = [Idle, Moving, Firing, Reloading, Destroyed]

TRANSITIONS = {
    Event.IDLE: [Transition(Reloading, Idle)],
    Event.MOVING: [Transition(Idle, Moving)],
    Event.FIRING: [Transition(Moving, Firing)],
    Event.RELOADING: [Transition(Firing, Reloading)],
    Event.DESTROYED: [Transition(Idle, Destroyed)]
}
