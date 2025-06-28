# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class LightState:
    state: bool


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

        state = False

        self._state = LightState(
            state,
        )

        # Set in ports

        self.control_port = self.addInPort("control")

        # Set out ports

        self.status_port = self.addOutPort("status")

        self.ta: float | str = float("inf")
        print(f"[{self.current_time:9.3f}][INIT] Light-{self.name}: {self._state}")

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
            if message == "on":
                state = True
            elif message == "off":
                state = False
            ta = 0

        # Update state context

        self._state.state = state

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Light-{self.name}: {self._state}")

    def outputFnc(self):
        output = {}

        true = True
        false = False

        def send(port, message):
            output[getattr(self, f"{port}_port")] = message

        ta = self.ta
        # Set state and port context

        status = self.status_port.getPortName()

        state = self._state.state

        # End state context

        send("status", "on" if state else "off")

        return output
