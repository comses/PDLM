from typing import Optional

# Import code for DEVS model representation:
from pypdevs.DEVS import *

from .light import Light
from .controller import Controller


class Root(CoupledDEVS):
    ta: float | str = float("inf")

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name: Optional[str] = None):

        # Initialize the super class
        super().__init__(name)

        # Coupled atomics

        self.controller1 = Controller(name="controller1")

        self.light1 = Light(name="light1")

        # Add submodels

        self.addSubModel(self.controller1)

        self.addSubModel(self.light1)

        # Add connections

        self.connectPorts(
            self.controller1.command_port,
            self.light1.control_port,
        )
