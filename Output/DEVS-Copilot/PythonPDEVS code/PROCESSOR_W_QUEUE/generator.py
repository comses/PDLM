# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class GeneratorState:
    count: int


class Generator(AtomicDEVS):
    ta: str | float
    _state: GeneratorState
    current_time: float = 0.0

    def timeAdvance(self) -> float:
        return self.ta

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name=None, id=None, kwargs=None):
        super(Generator, self).__init__(name)

        # State

        count = 0

        self._state = GeneratorState(
            count,
        )

        # Set out ports

        self.out_port = self.addOutPort("out")

        self.ta: float | str = float("11.0")
        print(f"[{self.current_time:9.3f}][INIT] Generator-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        count = self._state.count

        # End state context

        true = True
        false = False

        # Internal transition
        count += 1
        if count == 3:
            ta = float("inf")

        # Update state context

        self._state.count = count

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Generator-{self.name}: {self._state}")

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

        send(out, "job")

        return output
