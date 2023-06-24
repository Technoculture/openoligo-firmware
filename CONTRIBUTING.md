# For Contibuting

- Python 3.8+
- Poetry for Python dependency management.
- Ansible and sshpass for deploying to RPi (Should be present in local network)
- Docker (Optional)

# Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/techno/OpenOligo.git
cd OpenOligo
```

Replace <yourusername> with your actual GitHub username.

## 2. Install Python
Download and install Python from the official site.

## 3. Install Poetry
To install Poetry on your system, open a command prompt and run:

```bash
pip install poetry
```

## 4. Install Project Dependencies
To install the dependencies needed for the project, navigate to the project directory (where the pyproject.toml is located) in your terminal, and run:

```bash
poetry lock
poetry install
```

## 5. Run the Code

```bash
poetry run openoligo
```

# Using the Makefile

This project includes a Makefile that makes it easier to run common tasks. Here are the available targets:

- `make help`: Print help information about the available targets.
- `make lint`: Run linters on the code, including flake8, black (for code formatting checks), and isort (for import ordering checks).
- `make type`: Run the mypy type checker on the code.
- `make test`: Run tests

To use the Makefile, open your command prompt or terminal, navigate to the project directory, and run the `make` command followed by the target. For example, to run linters on the code, use:

```bash
make lint
make test
```

> Please make sure that you have make installed on your system. On Windows, you may need to install make via a package manager like Chocolatey, or use a POSIX compatibility layer like Git Bash or Cygwin.

# Deploying to a Raspberry Pi
- [Issue: Unable to install on Raspberry Pi](https://github.com/orgs/python-poetry/discussions/7057)

```sh
pip -U pip setuptools
pip install --only-binary cryptography poetry
```

- [How to install ZeroMQ on Raspberry Pi](https://github.com/MonsieurV/ZeroMQ-RPi)
