# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class LightState:
    status: str


class Light(AtomicDEVS):
    ta: str | float
    _state: LightState
    current_time: float = 0.0

    def timeAdvance(self) -> float:
        return self.ta

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name=None, id=None, kwargs=None):
        super(Light, self).__init__(name)

        # State

        status = "off"

        self._state = LightState(
            status,
        )

        # Set in ports

        self.in_port = self.addInPort("in")

        self.ta: float | str = float("inf")
        print(f"[{self.current_time:9.3f}][INIT] Light-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        status = self._state.status

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            status = message

        # Update state context

        self._state.status = status

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Light-{self.name}: {self._state}")
