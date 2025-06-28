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

        self.controller2 = Controller(name="controller2")

        self.controller3 = Controller(name="controller3")

        self.controller4 = Controller(name="controller4")

        self.controller5 = Controller(name="controller5")

        self.light = Light(name="light")

        # Add submodels

        self.addSubModel(self.controller1)

        self.addSubModel(self.controller2)

        self.addSubModel(self.controller3)

        self.addSubModel(self.controller4)

        self.addSubModel(self.controller5)

        self.addSubModel(self.light)

        # Add connections

        self.connectPorts(
            self.controller1.out_port,
            self.light.in_port,
        )

        self.connectPorts(
            self.controller2.out_port,
            self.light.in_port,
        )

        self.connectPorts(
            self.controller3.out_port,
            self.light.in_port,
        )

        self.connectPorts(
            self.controller4.out_port,
            self.light.in_port,
        )

        self.connectPorts(
            self.controller5.out_port,
            self.light.in_port,
        )
