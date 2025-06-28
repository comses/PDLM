# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class ControllerState:
    state: str


class Controller(AtomicDEVS):
    ta: str | float
    _state: ControllerState
    current_time: float = 0.0

    def timeAdvance(self) -> float:
        return self.ta

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name=None, id=None, kwargs=None):
        super(Controller, self).__init__(name)

        # State

        state = "off"

        self._state = ControllerState(
            state,
        )

        # Set out ports

        self.cmd_port = self.addOutPort("cmd")

        self.ta: float | str = float("10.0")
        print(f"[{self.current_time:9.3f}][INIT] Controller-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        state = self._state.state

        # End state context

        true = True
        false = False

        # Internal transition
        if state == "on":
            state = "off"
        else:
            state = "on"
        ta = 1

        # Update state context

        self._state.state = state

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Controller-{self.name}: {self._state}")

    def outputFnc(self):
        output = {}

        true = True
        false = False

        def send(port, message):
            output[getattr(self, f"{port}_port")] = message

        ta = self.ta
        # Set state and port context

        cmd = self.cmd_port.getPortName()

        state = self._state.state

        # End state context

        send(cmd, state)

        return output
