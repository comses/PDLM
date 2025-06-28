# Import code for DEVS model representation:
from pypdevs.DEVS import *
from dataclasses import dataclass

from random import random

rand = random

from numpy.random import poisson


@dataclass
class ControllerState:
    cycle_count: int
    light_state: bool


class Controller(AtomicDEVS):
    ta: str | float
    _state: ControllerState
    current_time: float = 0.0

    def timeAdvance(self) -> float:
        return self.ta

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name=None, id=None, kwargs=None):
        super(Controller, self).__init__(name)

        # State

        cycle_count = 0

        light_state = False

        self._state = ControllerState(
            cycle_count,
            light_state,
        )

        # Set in ports

        self.feedback_port = self.addInPort("feedback")

        # Set out ports

        self.command_port = self.addOutPort("command")

        self.ta: float | str = float("10.0")
        print(f"[{self.current_time:9.3f}][INIT] Controller-{self.name}: {self._state}")

    def intTransition(self):
        ta = self.ta
        self.current_time += self.ta
        # Set state context

        cycle_count = self._state.cycle_count

        light_state = self._state.light_state

        # End state context

        true = True
        false = False

        # Internal transition
        if cycle_count < 10:
            light_state = not light_state
            cycle_count += 1
            ta = 1.0
        else:
            ta = float("inf")

        # Update state context

        self._state.cycle_count = cycle_count

        self._state.light_state = light_state

        # End update state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][INT] Controller-{self.name}: {self._state}")

    def extTransition(self, inputs: dict):
        ta = self.ta
        self.current_time += self.elapsed
        # Set state context

        cycle_count = self._state.cycle_count

        light_state = self._state.light_state

        # End state context

        true = True
        false = False

        for input_port, message in inputs.items():
            port_name = input_port.getPortName()
            if message == "stop" and cycle_count == 10:
                light_state = False
                cycle_count += 1
                ta = 0

        # Update state context

        self._state.cycle_count = cycle_count

        self._state.light_state = light_state

        # End updade state context
        self.ta = ta
        print(f"[{self.current_time:9.3f}][EXT] Controller-{self.name}: {self._state}")

    def outputFnc(self):
        output = {}

        true = True
        false = False

        def send(port, message):
            output[getattr(self, f"{port}_port")] = message

        ta = self.ta
        # Set state and port context

        command = self.command_port.getPortName()

        cycle_count = self._state.cycle_count

        light_state = self._state.light_state

        # End state context

        send("command", "on" if light_state else "off")

        return output
