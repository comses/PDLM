# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class ProcessorState:
    state: str
    queue: str


class Processor(AtomicDEVS):
    ta: str | float
    _state: ProcessorState
    current_time: float = 0.0

    def timeAdvance(self) -> float:
        return self.ta

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name=None, id=None, kwargs=None):
        super(Processor, self).__init__(name)

        # State

        state = "idle"

        queue = "[]"

        self._state = ProcessorState(
            state,
            queue,
        )

        # Set in ports

        self.in_port = self.addInPort("in")

        # Set out ports

        self.out_port = self.addOutPort("out")

        self.ta: float | str = float("inf")
        print(f"[{self.current_time:9.3f}][INIT] Processor-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        state = self._state.state

        queue = self._state.queue

        # End state context

        true = True
        false = False

        # Internal transition
        if state == "busy":
            state = "idle"
            ta = 0
        elif queue:
            queue.pop(0)
            state = "busy"
            ta = 2

        # Update state context

        self._state.state = state

        self._state.queue = queue

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Processor-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        state = self._state.state

        queue = self._state.queue

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            if state == "idle":
                state = "busy"
                ta = 2
            else:
                queue.append(message)

        # Update state context

        self._state.state = state

        self._state.queue = queue

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Processor-{self.name}: {self._state}")

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

        queue = self._state.queue

        # End state context

        if state == "busy":
            send(out, "processed job")

        return output
