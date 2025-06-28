from typing import Optional

# Import code for DEVS model representation:
from pypdevs.DEVS import *

from .controller import Controller
from .light import Light


class Root(CoupledDEVS):
    ta: float | str = float("inf")

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name: Optional[str] = None):

        # Initialize the super class
        super().__init__(name)

        # Coupled atomics

        self.controller = Controller(name="controller")

        self.light1 = Light(name="light1")

        self.light2 = Light(name="light2")

        self.light3 = Light(name="light3")

        self.light4 = Light(name="light4")

        self.light5 = Light(name="light5")

        # Add submodels

        self.addSubModel(self.controller)

        self.addSubModel(self.light1)

        self.addSubModel(self.light2)

        self.addSubModel(self.light3)

        self.addSubModel(self.light4)

        self.addSubModel(self.light5)

        # Add connections

        self.connectPorts(
            self.controller.out_port,
            self.light1.in_port,
        )

        self.connectPorts(
            self.controller.out_port,
            self.light2.in_port,
        )

        self.connectPorts(
            self.controller.out_port,
            self.light3.in_port,
        )

        self.connectPorts(
            self.controller.out_port,
            self.light4.in_port,
        )

        self.connectPorts(
            self.controller.out_port,
            self.light5.in_port,
        )
