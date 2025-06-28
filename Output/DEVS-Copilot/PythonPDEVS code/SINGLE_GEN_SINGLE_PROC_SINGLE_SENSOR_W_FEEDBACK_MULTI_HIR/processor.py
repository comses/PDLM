# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class ProcessorState:
    queue: list
    state: str
    processing_time: int


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

        queue = []

        state = "'idle'"

        processing_time = 2

        self._state = ProcessorState(
            queue,
            state,
            processing_time,
        )

        # Set in ports

        self.in_1_port = self.addInPort("in_1")

        # Set out ports

        self.out_1_port = self.addOutPort("out_1")

        self.ta: float | str = float("inf")
        print(f"[{self.current_time:9.3f}][INIT] Processor-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        queue = self._state.queue

        state = self._state.state

        processing_time = self._state.processing_time

        # End state context

        true = True
        false = False

        # Internal transition
        if queue:
            queue.pop(0)
            ta = 2
        else:
            state = "idle"
            ta = float("inf")

        # Update state context

        self._state.queue = queue

        self._state.state = state

        self._state.processing_time = processing_time

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Processor-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        queue = self._state.queue

        state = self._state.state

        processing_time = self._state.processing_time

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            if port_name == "in_1":
                queue.append(message)
                if state == "idle":
                    state = "busy"
                    ta = 2

        # Update state context

        self._state.queue = queue

        self._state.state = state

        self._state.processing_time = processing_time

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

        out_1 = self.out_1_port.getPortName()

        queue = self._state.queue

        state = self._state.state

        processing_time = self._state.processing_time

        # End state context

        send("out_1", "processed_job")

        return output
