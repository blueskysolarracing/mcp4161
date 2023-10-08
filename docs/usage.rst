Usage
=====

Both high and low level interactions are supported by this library.

High-level Usage
----------------

The examples of high-level usages are shown below.

.. code-block:: pycon

   >>> from mcp4161 import MCP4161
   >>> from periphery import SPI
   >>> spi = SPI('/dev/spidev0.0', 3, 1e6)
   >>> mcp4161 = MCP4161(spi)
   >>> mcp4161.set_step(123)

Low-level Usage
---------------

The examples of low-level usages are shown below.

.. code-block:: pycon

   >>> from mcp4161 import MCP4161
   >>> from periphery import SPI
   >>> spi = SPI('/dev/spidev0.0', 3, 1e6)
   >>> mcp4161 = MCP4161(spi)
   >>> mcp4161.write_data(MCP4161.MemoryAddress.VOLATILE_WIPER_0, 123)
   >>> mcp4161.increment(MCP4161.MemoryAddress.VOLATILE_WIPER_0)
   >>> mcp4161.read_data(MCP4161.MemoryAddress.VOLATILE_WIPER_0)
   124
   >>> mcp4161.command(
   ...     MCP4161.WriteData(MCP4161.MemoryAddress.VOLATILE_WIPER_0, 0),
   ...     MCP4161.Increment(MCP4161.MemoryAddress.VOLATILE_WIPER_0),
   ...     MCP4161.ReadData(MCP4161.MemoryAddress.VOLATILE_WIPER_0),
   ... )
   [None, None, 1]
