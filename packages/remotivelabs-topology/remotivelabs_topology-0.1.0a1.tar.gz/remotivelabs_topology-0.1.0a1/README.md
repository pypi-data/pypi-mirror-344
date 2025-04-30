# RemotiveTopology framework

RemotiveLabs RemotiveTopology framework allows developers to easily create and run ECU stubs and control their behavior.

## Installation

```bash
pip install remotivelabs-topology
```

## Usage

TODO

## Logging

This library uses Python's standard `logging` module. By default, the library does not configure any logging handlers, allowing applications to fully control their logging setup.

To enable logs from this library in your application or tests, configure logging as follows:

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("remotivelabs.topology").setLevel(logging.DEBUG)
```

For more advanced configurations, refer to the [Python logging documentation](https://docs.python.org/3/library/logging.html).

## Project Links

- [Documentation](https://docs.remotivelabs.com/)
- [Issues](mailto:support@remotivelabs.com)
