# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class SensorbState:
    count: int


class Sensorb(AtomicDEVS):
    ta: str | float
    _state: SensorbState
    current_time: float = 0.0

    def timeAdvance(self) -> float:
        return self.ta

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name=None, id=None, kwargs=None):
        super(Sensorb, self).__init__(name)

        # State

        count = 0

        self._state = SensorbState(
            count,
        )

        # Set in ports

        self.in_port = self.addInPort("in")

        # Set out ports

        self.out_port = self.addOutPort("out")

        self.ta: float | str = float("inf")
        print(f"[{self.current_time:9.3f}][INIT] Sensorb-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        count = self._state.count

        # End state context

        true = True
        false = False

        # Internal transition
        if count == 5:
            count = 0
            ta = 0

        # Update state context

        self._state.count = count

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Sensorb-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        count = self._state.count

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            count += 1
            if count == 5:
                ta = 0

        # Update state context

        self._state.count = count

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Sensorb-{self.name}: {self._state}")

    def outputFnc(self):
        output = {}

        true = True
        false = False

        def send(port, message):
            output[getattr(self, f"{port}_port")] = message

        ta = self.ta
        # Set state and port context

        out = self.out_port.getPortName()

        count = self._state.count

        # End state context

        send(out, "stop")

        return output
