from typing import Optional

# Import code for DEVS model representation:
from pypdevs.DEVS import *

from .sensor import Sensor
from .controller import Controller


class Root(CoupledDEVS):
    ta: float | str = float("inf")

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name: Optional[str] = None):

        # Initialize the super class
        super().__init__(name)

        # Coupled atomics

        self.Controller1 = Controller(name="Controller1")

        self.Controller2 = Controller(name="Controller2")

        self.Controller3 = Controller(name="Controller3")

        self.Sensor = Sensor(name="Sensor")

        # Add submodels

        self.addSubModel(self.Controller1)

        self.addSubModel(self.Controller2)

        self.addSubModel(self.Controller3)

        self.addSubModel(self.Sensor)

        # Add connections

        self.connectPorts(
            self.Controller1.control_port,
            self.Sensor.cycle_port,
        )

        self.connectPorts(
            self.Controller2.control_port,
            self.Sensor.cycle_port,
        )

        self.connectPorts(
            self.Controller3.control_port,
            self.Sensor.cycle_port,
        )

        self.connectPorts(
            self.Sensor.feedback_port,
            self.Controller1.stop_port,
        )

        self.connectPorts(
            self.Sensor.feedback_port,
            self.Controller2.stop_port,
        )

        self.connectPorts(
            self.Sensor.feedback_port,
            self.Controller3.stop_port,
        )
