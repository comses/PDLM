from typing import Optional

# Import code for DEVS model representation:
from pypdevs.DEVS import *

from .sensor import Sensor
from .processor import Processor


class Processorsensor(CoupledDEVS):
    ta: float | str = float("inf")

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name: Optional[str] = None):

        # Initialize the super class
        super().__init__(name)

        # Coupled atomics

        self.processor = Processor(name="processor")

        self.sensor = Sensor(name="sensor")

        # Add submodels

        self.addSubModel(self.processor)

        self.addSubModel(self.sensor)

        # Add connections

        self.connectPorts(
            self.processor.out_1_port,
            self.sensor.in_port,
        )
