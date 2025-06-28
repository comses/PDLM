# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class ProcessorState:
    queue: str
    processingTime: int
    busy: int


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

        queue = "[]"

        processingTime = 2

        busy = 0

        self._state = ProcessorState(
            queue,
            processingTime,
            busy,
        )

        # Set in ports

        self.in_1_port = self.addInPort("in_1")

        self.in_2_port = self.addInPort("in_2")

        # Set out ports

        self.out_1_port = self.addOutPort("out_1")

        self.out_2_port = self.addOutPort("out_2")

        self.ta: float | str = float("inf")
        print(f"[{self.current_time:9.3f}][INIT] Processor-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        queue = self._state.queue

        processingTime = self._state.processingTime

        busy = self._state.busy

        # End state context

        true = True
        false = False

        # Internal transition
        if busy:
            busy = False
            ta = float("inf")

        # Update state context

        self._state.queue = queue

        self._state.processingTime = processingTime

        self._state.busy = busy

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Processor-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        queue = self._state.queue

        processingTime = self._state.processingTime

        busy = self._state.busy

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            queue.append(message)
            if not busy:
                busy = True
                ta = processingTime

        # Update state context

        self._state.queue = queue

        self._state.processingTime = processingTime

        self._state.busy = busy

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

        out_2 = self.out_2_port.getPortName()

        queue = self._state.queue

        processingTime = self._state.processingTime

        busy = self._state.busy

        # End state context

        if "JobA" in queue[0]:
            send(out_1, queue.pop(0))
        elif "JobB" in queue[0]:
            send(out_2, queue.pop(0))

        return output
