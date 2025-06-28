# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class ControllerState:
    status: str


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

        status = "off"

        self._state = ControllerState(
            status,
        )

        # Set out ports

        self.command_port = self.addOutPort("command")

        self.ta: float | str = float("10.0")
        print(f"[{self.current_time:9.3f}][INIT] Controller-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        status = self._state.status

        # End state context

        true = True
        false = False

        # Internal transition
        if status == "on":
            status = "off"
            ta = 10
        else:
            status = "on"
            ta = 10

        # Update state context

        self._state.status = status

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

        command = self.command_port.getPortName()

        status = self._state.status

        # End state context

        send("command", status)

        return output
