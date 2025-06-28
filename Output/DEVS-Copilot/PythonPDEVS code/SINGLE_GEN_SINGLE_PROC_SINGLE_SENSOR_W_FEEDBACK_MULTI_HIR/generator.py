# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class GeneratorState:
    job_number: int
    state: str


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

        job_number = 1

        state = "'active'"

        self._state = GeneratorState(
            job_number,
            state,
        )

        # Set in ports

        self.stop_port = self.addInPort("stop")

        # Set out ports

        self.out_port = self.addOutPort("out")

        self.ta: float | str = float("3.0")
        print(f"[{self.current_time:9.3f}][INIT] Generator-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        job_number = self._state.job_number

        state = self._state.state

        # End state context

        true = True
        false = False

        # Internal transition
        job_number += 1

        # Update state context

        self._state.job_number = job_number

        self._state.state = state

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Generator-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        job_number = self._state.job_number

        state = self._state.state

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            if port_name == "stop":
                state = "passive"
                ta = float("inf")

        # Update state context

        self._state.job_number = job_number

        self._state.state = state

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Generator-{self.name}: {self._state}")

    def outputFnc(self):
        output = {}

        true = True
        false = False

        def send(port, message):
            output[getattr(self, f"{port}_port")] = message

        ta = self.ta
        # Set state and port context

        out = self.out_port.getPortName()

        job_number = self._state.job_number

        state = self._state.state

        # End state context

        send("out", f"Job{job_number}")

        return output
