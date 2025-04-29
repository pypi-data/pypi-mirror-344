# template-python
Simple README.md for a Python project template.

## Install
To install the library run: `pip install change-me`

## Development
0. Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
1. `make init` to create the virtual environment and install dependencies
2. `make format` to format the code and check for errors
3. `make test` to run the test suite
4. `make clean` to delete the temporary files and directories
5. `poetry publish --build` to build and publish to https://pypi.org/project/change-me


## Usage
```
"""Basic docstring for my module."""

from loguru import logger

def main() -> None:
    """Run a simple demonstration."""
logger.info("Hello World!")

if __name__ == "__main__":
    main()
```
