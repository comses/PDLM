from typing import Optional

# Import code for DEVS model representation:
from pypdevs.DEVS import *

from .processor import Processor
from .generator import Generator


class Root(CoupledDEVS):
    ta: float | str = float("inf")

    def __lt__(self, other):
        return self.name < other.name

    def __init__(self, name: Optional[str] = None):

        # Initialize the super class
        super().__init__(name)

        # Coupled atomics

        self.generator = Generator(name="generator")

        self.processor = Processor(name="processor")

        # Add submodels

        self.addSubModel(self.generator)

        self.addSubModel(self.processor)

        # Add connections

        self.connectPorts(
            self.generator.out_port,
            self.processor.in_port,
        )
