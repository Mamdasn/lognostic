# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2024-03-06

### Added

- Initial setup of the PyPI Development Environment.
- Statistical functionalities for analyzing `LogRecords`.
- Unit tests covering class methods and thread-safety.
- `pandas` package dependency in `pyproject.toml` for statistics calculation.
- MyPy typing annotations to source `.py` files for better type validation.
- `pandas-stubs` for MyPy type validation, enhancing static type checking.
- Pre-commit hooks setup to enforce code style and quality checks.
- A Dockerfile to define the build environment and run tests, ensuring a consistent development environment.
- Documentation docstrings across `lognostic`, making the API self-documenting and easier to understand for developers.

### Changed

- Merged `stats_manager` and `lognostic` modules to streamline the package structure.
- Bumped Python version from 3.8 to 3.9, taking advantage of newer language features.
- Reduced redundancy by minimizing repeated code across the package, improving maintainability.

### Fixed

- Applied fixes from `isort` to ensure consistent import ordering.
- General code quality improvements through the application of pre-commit checks.

### Security

- N/A


[Unreleased]: https://github.com/Mamdasn/lognostic/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/Mamdasn/lognostic/releases/tag/v0.0.1
