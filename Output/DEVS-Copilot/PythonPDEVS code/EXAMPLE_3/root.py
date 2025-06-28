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

        self.controller_instance = Controller(name="controller_instance")

        self.light_instance = Light(name="light_instance")

        # Add submodels

        self.addSubModel(self.controller_instance)

        self.addSubModel(self.light_instance)

        # Add connections

        self.connectPorts(
            self.controller_instance.out_port,
            self.light_instance.in_port,
        )
