# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class SensorState:
    state: str


class Sensor(AtomicDEVS):
    ta: str | float
    _state: SensorState
    current_time: float = 0.0

    def timeAdvance(self) -> float:
        return self.ta

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name=None, id=None, kwargs=None):
        super(Sensor, self).__init__(name)

        # State

        state = "off"

        self._state = SensorState(
            state,
        )

        # Set in ports

        self.status_port = self.addInPort("status")

        self.ta: float | str = float("inf")
        print(f"[{self.current_time:9.3f}][INIT] Sensor-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        state = self._state.state

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            if port_name == "status":
                state = message

        # Update state context

        self._state.state = state

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Sensor-{self.name}: {self._state}")
