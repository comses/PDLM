from typing import Optional

# Import code for DEVS model representation:
from pypdevs.DEVS import *

from .light import Light
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

        self.controller_instance = Controller(name="controller_instance")

        self.light_instance = Light(name="light_instance")

        self.sensor_instance = Sensor(name="sensor_instance")

        # Add submodels

        self.addSubModel(self.controller_instance)

        self.addSubModel(self.light_instance)

        self.addSubModel(self.sensor_instance)

        # Add connections

        self.connectPorts(
            self.controller_instance.command_port,
            self.light_instance.control_port,
        )

        self.connectPorts(
            self.light_instance.status_port,
            self.sensor_instance.light_status_port,
        )

        self.connectPorts(
            self.sensor_instance.control_feedback_port,
            self.controller_instance.feedback_port,
        )
