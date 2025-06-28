from typing import Optional

# Import code for DEVS model representation:
from pypdevs.DEVS import *

from .sensor_b import Sensorb
from .processor import Processor
from .sensor_a import Sensora
from .generator_a import Generatora
from .generator_b import Generatorb


class Root(CoupledDEVS):
    ta: float | str = float("inf")

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name: Optional[str] = None):

        # Initialize the super class
        super().__init__(name)

        # Coupled atomics

        self.Generator_A = Generatora(name="Generator_A")

        self.Generator_B = Generatorb(name="Generator_B")

        self.Processor = Processor(name="Processor")

        self.Sensor_A = Sensora(name="Sensor_A")

        self.Sensor_B = Sensorb(name="Sensor_B")

        # Add submodels

        self.addSubModel(self.Generator_A)

        self.addSubModel(self.Generator_B)

        self.addSubModel(self.Processor)

        self.addSubModel(self.Sensor_A)

        self.addSubModel(self.Sensor_B)

        # Add connections

        self.connectPorts(
            self.Generator_A.out_port,
            self.Processor.in_1_port,
        )

        self.connectPorts(
            self.Generator_B.out_1_port,
            self.Processor.in_1_port,
        )

        self.connectPorts(
            self.Generator_B.out_2_port,
            self.Processor.in_2_port,
        )

        self.connectPorts(
            self.Processor.out_1_port,
            self.Sensor_A.in_port,
        )

        self.connectPorts(
            self.Processor.out_2_port,
            self.Sensor_B.in_port,
        )

        self.connectPorts(
            self.Sensor_A.out_port,
            self.Generator_A.stop_port,
        )

        self.connectPorts(
            self.Sensor_B.out_port,
            self.Generator_B.stop_port,
        )
