# По пути

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
> poetry install --only main
```

##### Linux:

Initialization and launch of the virtual environment with poetry.

```shell
$ curl -sSL https://install.python-poetry.org | python3 -

$ echo "export PATH=$PATH:~/.local/share/pypoetry/venv/bin" >> ~/.bashrc

$ bash

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
 poetry run pre-commit install
```

#### Commands

- `poetry run black src/*` – launch style checker.
- `poetry run pylint src/*` – launch linter.
- `poetry run python -m src.main` – launch app.

### Docker

Starting all containers:

`docker-compose up`

Postgres database deployed with options specified in `.env` on port `5432`.

Database management systems adminer deployed on port `8080` and is available at [this link](http://localhost:8080/) (for connection by ssh try [this link](http://0.0.0.0:8080)).

In order to enter the database, you need to specify parameters similar to the parameters from `.env`, in the _"Server"_ field you need to specify `postgres:5432`.

## Authors

* **Nelin Maxim** – [GitHub](https://github.com/Nelin-M)
* **Shatilova Daria** – [GitHub](https://github.com/solovyova-1996)
* **Zharkov Valery** – [GitHub](https://github.com/Lykor)
* **Manyakin Vyacheslav** – [GitHub](https://github.com/vmanyakin)
* **Ramil Arsymbekov** – [GitHub](https://github.com/arsy-off)
* **Wagner Roman** – [GitHub](https://github.com/Cartez55)
