# Yala API
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

### Requirements
- python>=3.9.18 (create a new virtual environment called `venv`)
- docker
- docker compose (we are using docker compose instead of docker-compose)
- At least 4 GB dedicated RAM for docker
- We are used to use PyCharm, but it's not mandatory

### Set the virtual env

```console
$ python -m venv venv
```

#### Install requirements

```console
$ make install
```

#### Build docker image

```console
$ make build
```

#### Start services

```console
$ make start
```

#### Run migrations

```console
$ make migrate
```

#### Create super user

Enter super user creds after running:

```console
$ make createsuperuser
```

Now, you should be able to go to [admin](http://localhost:8000/admin) with you super user creds

---
### Linting

```console
$ make lint
```
---
### Remove docker containers

```console
$ make stop
```
