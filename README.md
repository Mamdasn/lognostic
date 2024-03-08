# lognostic

[![PyPI](https://img.shields.io/pypi/v/lognostic?style=flat-square)](https://pypi.python.org/pypi/lognostic/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lognostic?style=flat-square)](https://pypi.python.org/pypi/lognostic/)
[![PyPI - License](https://img.shields.io/pypi/l/lognostic?style=flat-square)](https://pypi.python.org/pypi/lognostic/)


---

**Documentation**: [https://Mamdasn.github.io/lognostic](https://Mamdasn.github.io/lognostic)

**Source Code**: [https://github.com/Mamdasn/lognostic](https://github.com/Mamdasn/lognostic)

**PyPI**: [https://pypi.org/project/lognostic/](https://pypi.org/project/lognostic/)

---

`lognostic` is a lightweight, efficient Python package designed to seamlessly integrate into existing Python applications to provide logging statistics. This package caters to development teams seeking to optimize logging performance, diagnose issues, and understand logging loads without introducing significant overhead or complexity into their applications.

## Installation

```sh
pip install lognostic
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.9+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Custom logging Handler

The `lognostic` module can be integrated into logging subsystems by employing a custom logging handler:

```python
class LogHandler(logging.Handler):
    def __init__(self, lognostic: Lognostic):
        super().__init__()
        self._lognostic = lognostic

    def emit(self, log_record: logging.LogRecord):
        self._lognostic.record(log_record)
```

A `Lognostic` instance should be given to the custom logging handler, so later logging statistics can be obtained:

```python
lognostic = Lognostic()
loghandler = LogHandler(lognostic)
logger.addHandler(loghandler)

logger.info('This is a test log message')

lognostic.total_size() # -> returns 26
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings found in the source code.


### Testing
Run unit tests using
```sh
pytest tests
```

> **_Automated test runs_**: The `lognostic` package is automatically tested through python versions 3.9 to 3.12 using GitHub's CI/CD pipeline.  

### Docker Usage

Build the image of the Dockerfile using
```sh
docker build -t lognostic .
```
Run the image with
```sh
docker run --name lognostic_instance lognostic
```

> The docker builds the envioronment followed by running the pre-commits and unit tests.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

## Future features and improvements
+ Data persistency: Store statistics on the disk persistency for future historical logging analysis.
+ Logging Dashboard: A web dashboard to visualize logging statistics in real-time, allowing teams to monitor logging load dynamically.
+ Throw warning/error messages if certain logging thresholds are met, such as an unusually high logging rate, to quickly identify potential issues.
---

This project was generated using the [python-package-cookiecutter](https://github.com/Mamdasn/python-package-cookiecutter) template.
