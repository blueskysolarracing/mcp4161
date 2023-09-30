from dataclasses import dataclass
from enum import IntEnum
from typing import ClassVar
from warnings import warn

from periphery import SPI


@dataclass
class MCP4161:
    """A Python driver for Microchip Technology MCP4161 7/8-Bit
    Single/Dual SPI Digital POT with Non-Volatile Memory
    """

    class MemoryAddress(IntEnum):
        """The enum class for memory addresses."""

        VOLATILE_WIPER_0: int = 0x00
        """The volatile wiper 0."""
        NON_VOLATILE_WIPER_0: int = 0x02
        """The non-volatile wiper 0."""
        VOLATILE_TCON_REGISTER: int = 0x04
        """The volatile TCON register."""
        STATUS_REGISTER: int = 0x05
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

    SPI_MODES: ClassVar[tuple[int, int]] = 0b00, 0b11
    """The supported spi modes."""
    MAX_SPI_MAX_SPEED: ClassVar[float] = 10e6
    """The supported maximum spi maximum speed."""
    SPI_BIT_ORDER: ClassVar[str] = 'msb'
    """The supported spi bit order."""
    SPI_WORD_BIT_COUNT: ClassVar[int] = 8
    """The supported spi number of bits per word."""
    STEP_RANGE: ClassVar[range] = range(257)
    """The step range."""
    MEMORY_ADDRESS_OFFSET: ClassVar[int] = 4
    """The memory address offset for the command byte."""
    COMMAND_BITS_OFFSET: ClassVar[int] = 2
    """The command bits offset for the command byte."""
    spi: SPI
    """The SPI."""

    def __post_init__(self) -> None:
        if self.spi.mode not in self.SPI_MODES:
            raise ValueError('unsupported spi mode')
        elif self.spi.max_speed > self.MAX_SPI_MAX_SPEED:
            raise ValueError('unsupported spi maximum speed')
        elif self.spi.bit_order != self.SPI_BIT_ORDER:
            raise ValueError('unsupported spi bit order')
        elif self.spi.bits_per_word != self.SPI_WORD_BIT_COUNT:
            raise ValueError('unsupported spi number of bits per word')

        if self.spi.extra_flags:
            warn(f'unknown spi extra flags {self.spi.extra_flags}')

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
                (memory_address << self.MEMORY_ADDRESS_OFFSET)
                | (self.CommandBits.WRITE_DATA << self.COMMAND_BITS_OFFSET)
                | (data >> self.SPI_WORD_BIT_COUNT)
            ),
            data & ((1 << self.SPI_WORD_BIT_COUNT) - 1),
        ]

        self.spi.transfer(transmitted_data)

    def increment(self, memory_address: int) -> None:
        """Increment the data at the memory address.

        :param memory_address: The memory address.
        :return: ``None``.
        """
        transmitted_data = [
            (memory_address << self.MEMORY_ADDRESS_OFFSET)
            | (self.CommandBits.INCREMENT << self.COMMAND_BITS_OFFSET),
        ]

        self.spi.transfer(transmitted_data)

    def decrement(self, memory_address: int) -> None:
        """Decrement the data at the memory address.

        :param memory_address: The memory address.
        :return: ``None``.
        """
        transmitted_data = [
            (memory_address << self.MEMORY_ADDRESS_OFFSET)
            | (self.CommandBits.DECREMENT << self.COMMAND_BITS_OFFSET),
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
