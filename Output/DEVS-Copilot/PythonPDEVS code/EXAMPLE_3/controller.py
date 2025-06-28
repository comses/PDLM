# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class ControllerState:
    state: str
    time_advance: float


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

        time_advance = float("10")

        self._state = ControllerState(
            state,
            time_advance,
        )

        # Set out ports

        self.out_port = self.addOutPort("out")

        self.ta: float | str = float("10.0")
        print(f"[{self.current_time:9.3f}][INIT] Controller-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        state = self._state.state

        time_advance = self._state.time_advance

        # End state context

        true = True
        false = False

        # Internal transition
        if state == "on":
            state = "off"
        else:
            state = "on"
        ta = time_advance

        # Update state context

        self._state.state = state

        self._state.time_advance = time_advance

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

        out = self.out_port.getPortName()

        state = self._state.state

        time_advance = self._state.time_advance

        # End state context

        send("out", state)

        return output
