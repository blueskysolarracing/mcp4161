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
        """The non-volatile wiper 0."""
        VOLATILE_TCON_REGISTER: int = 0b0010
        """The volatile TCON register."""
        STATUS_REGISTER: int = 0b0010
        """The status register."""

    class CommandBits(IntEnum):
        """The enum class for command bits."""

        READ_DATA: int = 0b11
        """The read data command."""
        WRITE_DATA: int = 0b00
        """The write data command."""
        INCREMENT: int = 0b01
        """The increment command."""
        DECREMENT: int = 0b10
        """The decrement command."""

    STEP_RANGE: ClassVar[range] = range(257)
    """The step range."""
    spi: SPI
    """The SPI."""

    def read_data(self, memory_address: int) -> list[int]:
        """Read the data at the memory address.

        :param memory_address: The memory address.
        :return: The read data.
        """
        raise NotImplementedError('reading not supported')

    def write_data(self, memory_address: int, data: int) -> None:
        """Write the data at the memory address.

        :param memory_address: The memory address.
        :param data: The data.
        :return: ``None``.
        """
        transmitted_data = [
            (
                (memory_address << 4)
                | (self.CommandBits.WRITE_DATA << 2)
                | (data >> 8)
            ),
            data & ((1 << 8) - 1),
        ]

        self.spi.transfer(transmitted_data)

    def increment(self, memory_address: int) -> None:
        """Increment the data at the memory address.

        :param memory_address: The memory address.
        :return: ``None``.
        """
        transmitted_data = [
            (memory_address << 4) | (self.CommandBits.INCREMENT << 2),
        ]

        self.spi.transfer(transmitted_data)

    def decrement(self, memory_address: int) -> None:
        """Decrement the data at the memory address.

        :param memory_address: The memory address.
        :return: ``None``.
        """
        transmitted_data = [
            (memory_address << 4) | (self.CommandBits.DECREMENT << 2),
        ]

        self.spi.transfer(transmitted_data)

    def set_step(self, step: int, eeprom: bool = False) -> None:
        """Set the volatile or non-volatile wiper step.

        :param step: The step.
        :param eeprom: ``True`` if non-volatile, otherwise ``False``.
        :return: ``None``.
        """
        if eeprom:
            memory_address = self.MemoryAddress.NON_VOLATILE_WIPER_0
        else:
            memory_address = self.MemoryAddress.VOLATILE_WIPER_0

        if step not in self.STEP_RANGE:
            raise ValueError('invalid step')

        self.write_data(memory_address, step)
