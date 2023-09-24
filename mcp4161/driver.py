from dataclasses import dataclass
from enum import IntEnum
from typing import ClassVar

from periphery import SPI


@dataclass
class MCP4161:
    """A Python driver for Microchip Technology MCP4161 7/8-Bit
    Single/Dual SPI Digital POT with Non-Volatile Memory
    """

    class MemoryAddress(IntEnum):
        """The enum class for memory addresses."""

        VOLATILE_WIPER_0: int = 0b0000
        """The volatile wiper 0."""
        NON_VOLATILE_WIPER_0: int = 0b0010
        """The non-volatile wiper 1."""

    class CommandBits(IntEnum):
        """The enum class for command bits."""

        WRITE_DATA: int = 0b00
        """The write data command."""
        READ_DATA: int = 0b11
        """The read data command."""

    STEP_RANGE: ClassVar[range] = range(257)
    spi: SPI
    """The SPI."""

    def write_data(
            self,
            memory_address: MemoryAddress,
            data: int,
    ) -> list[int]:
        transmitted_data = [
            (
                (memory_address << 4)
                | (self.CommandBits.WRITE_DATA << 2)
                | (data >> 8)
            ),
            data & ((1 << 8) - 1),
        ]

        received_data = self.spi.transfer(transmitted_data)

        assert isinstance(received_data, list)

        return received_data

    def set_step(self, step: int, eeprom: bool = False) -> None:
        if eeprom:
            memory_address = self.MemoryAddress.NON_VOLATILE_WIPER_0
        else:
            memory_address = self.MemoryAddress.VOLATILE_WIPER_0

        if step not in self.STEP_RANGE:
            raise ValueError('invalid step')

        self.write_data(memory_address, step)
