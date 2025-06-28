# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class SensorState:
    count: int
    prepare_stop_signal: bool


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

        count = 0

        prepare_stop_signal = False

        self._state = SensorState(
            count,
            prepare_stop_signal,
        )

        # Set in ports

        self.in_port = self.addInPort("in")

        # Set out ports

        self.out_port = self.addOutPort("out")

        self.ta: float | str = float("inf")
        print(f"[{self.current_time:9.3f}][INIT] Sensor-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        count = self._state.count

        prepare_stop_signal = self._state.prepare_stop_signal

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            count += 1
            if count == 5:
                prepare_stop_signal = True

        # Update state context

        self._state.count = count

        self._state.prepare_stop_signal = prepare_stop_signal

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Sensor-{self.name}: {self._state}")

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

        prepare_stop_signal = self._state.prepare_stop_signal

        # End state context

        if count == 5:
            send("out", "stop")

        return output
