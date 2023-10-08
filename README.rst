=======
MCP4161
=======

MCP4161 is a Python driver for Microchip Technology MCP4161 7/8-Bit Single/Dual
SPI Digital POT with Non-Volatile Memory.

Features
--------

- High-level hardware usage.
- Low-level hardware usage.

Installation
------------

.. code-block:: bash

   pip install mcp4161

Usage
-----

Below shows a sample usage of MCP4161.

.. code-block:: python

   from mcp4161 import MCP4161
   from periphery import SPI

   spi = SPI('/dev/spidev0.0', 3, 1e6)
   mcp4161 = MCP4161(spi)

   mcp4161.set_step(123)

Testing and Validation
----------------------

MCP4161 has extensive test coverage, passes mypy static type checking with
strict parameter, and has been validated through extensive use in real-life
scenarios.

Contributing
------------

Contributions are welcome! Please read our Contributing Guide for more
information.

License
-------

MCP4161 is distributed under the MIT license.
