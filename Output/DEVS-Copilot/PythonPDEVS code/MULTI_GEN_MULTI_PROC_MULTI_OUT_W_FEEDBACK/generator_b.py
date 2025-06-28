# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class GeneratorbState:
    count: int
    active: int


class Generatorb(AtomicDEVS):
    ta: str | float
    _state: GeneratorbState
    current_time: float = 0.0

    def timeAdvance(self) -> float:
        return self.ta

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name=None, id=None, kwargs=None):
        super(Generatorb, self).__init__(name)

        # State

        count = 1

        active = 1

        self._state = GeneratorbState(
            count,
            active,
        )

        # Set in ports

        self.stop_port = self.addInPort("stop")

        # Set out ports

        self.out_1_port = self.addOutPort("out_1")

        self.out_2_port = self.addOutPort("out_2")

        self.ta: float | str = float("6.0")
        print(f"[{self.current_time:9.3f}][INIT] Generatorb-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        count = self._state.count

        active = self._state.active

        # End state context

        true = True
        false = False

        # Internal transition
        if active:
            count += 1

        # Update state context

        self._state.count = count

        self._state.active = active

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Generatorb-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        count = self._state.count

        active = self._state.active

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            if port_name == "stop":
                active = False
                ta = float("inf")

        # Update state context

        self._state.count = count

        self._state.active = active

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Generatorb-{self.name}: {self._state}")

    def outputFnc(self):
        output = {}

        true = True
        false = False

        def send(port, message):
            output[getattr(self, f"{port}_port")] = message

        ta = self.ta
        # Set state and port context

        out_1 = self.out_1_port.getPortName()

        out_2 = self.out_2_port.getPortName()

        count = self._state.count

        active = self._state.active

        # End state context

        send(out_1, "JobB1" + str(count))
        send(out_2, "JobB2" + str(count))

        return output
