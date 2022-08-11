# Deliveery bot

## Getting Started

_Run all commands from the root of the project_

### Preparing

#### Install python 3.10.x

##### Windows:

[download python 3.10](https://www.python.org/downloads/release/python-3100/).

##### Linux:

```shell
$ sudo apt-get install python3.10
```

#### Install dependencies

##### Windows:

Initialization and launch of the virtual environment with poetry.

```shell
> pip install poetry

> poetry env use PATH_TO_YOUR_PYTHON_3.10
```

Install _Microsoft C++ Build Tools_ 14.0 or greater.

Install dependencies.

```shell
> poetry install --no-dev
```

##### Linux:

Initialization and launch of the virtual environment with poetry.

```shell
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3.10

$ poetry env use python3.10
```

Install dependencies.

```shell
$ sudo apt-get install python3.10-dev

$ poetry install --no-dev
```

#### Environment variables

Rename the `.env.dist` file to `.env` and fill in the indicated fields.

### Launch

```shell
 poetry run python -m src.main
```

### Stopping

```shell
 ctrl + c
```

### Dev. env.

#### Preparation

##### Pre-commit

To enable pre-commit on the current repository:

```shell
 pre-commit install
```

#### Commands

- `poetry run black src/*` – launch style checker.
- `poetry run pylint src/*` – launch linter.
- `poetry run python -m src.main` – launch app.


## Authors

* **Nelin Maxim** – [GitHub](https://github.com/Nelin-M)