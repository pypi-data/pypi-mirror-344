# pyftdi-shell

A simple prompt to a FTDI serial line based on PyFtdi.
The supported interfaces are:
- I2C
- SPI
- GPIO

## Installation

```sh
pip install pyftdi-shell
```

## Usage

Open a GPIO prompt on FTDI channel 4

```sh
pyftdi-shell gpio ftdi:///4
```

Open a I2C prompt on FTDI channel 2

```sh
pyftdi-shell i2c ftdi:///2
```

> The URL fromat follows PyFtdi [documentation](https://eblot.github.io/pyftdi/urlscheme.html)
