# saas-ips

[![PyPI](https://img.shields.io/pypi/v/saas-ips.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/saas-ips.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/saas-ips)][pypi status]

[pypi status]: https://pypi.org/project/saas-ips/

`saas-ips` is a simple Python package and CLI tool to retrieve formatted lists of known SaaS based services IP ranges.

> If you have ever been looking at logs and want to know if an IP belongs to X service? That's the why


## What is saas-ips?

If you have ever been looking through logs, investigating, etc. and want to know if an IP belongs to SaaS service (Microsoft, Google, etc.)?

Well, `saas-ips` is a simeple little utility to collect these from different services and create a single model that can be consumed by another package or simple on the command line.

## Features

- Collect a list of known IPs for some SaaS Services
- Output the list of IPs to a JSON file
- Profit?

Currently we support the following SaaS services:

* Atlassian
* Microsoft Azure
* Box
* Fastly
* Google
* Microsoft O365

> You can find an example of the JSON output [here](./latest-output.json)

## Installation

You can install blocker via [pip] from [PyPI]:

```bash
$ pip install saas-ips
```

If you are using `poetry` (recommended) you can add it to your package using

```bash
poetry add saas-ips
```

## Usage

Below is the command line reference but you can also use the current version of `saas-ips` to retrieve the help by typing ```saas-ips --help```.

```bash
NAME
    saas-ips - Collector class.

SYNOPSIS
    saas-ips COMMAND

DESCRIPTION
    Collector class.

COMMANDS
    COMMAND is one of the following:

     run
       Run the collector.
```

To collect a list of IPs from the supported SaaS services, you can run the following at the command line:

```bash
saas-ips run --output ./output.json
```

If you are using poetry, then use:

```bash
poetry run saas-ips run --output ./output.json
```

## Developmemt

You can clone the repositry and begin development using

```bash
git clone https://github.com/MSAdministrator/saas-ips.git
cd saas-ips
poetry install
```

If you are using `pyenv` to manage your enviroments you can set a config option in poetry to use the set pyenv version of python by running this:

```bash
poetry config virtualenvs.create true
poetry install
```

## Issues

If you encounter any problems, please [file an issue](https://github.com/MSAdministrator/saas-ips/issues/new) along with a detailed description.

If you would like other services to be added, please also file an issue!
