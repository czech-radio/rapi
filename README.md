# RAPI

[![main](https://github.com/czech-radio/rapi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/czech-radio/rapi/actions/workflows/main.yml) ![version](https://img.shields.io/badge/version-0.9.0-blue.svg) ![language](https://img.shields.io/badge/language-Python-blue.svg) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/238d42622d25443c8dc71b60e38efb6b)](https://app.codacy.com/gh/czech-radio/rapi/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) ![GitHub stars](https://img.shields.io/github/stars/czech-radio/rapi?style=social) 

**Python REST API client for [mujrozhlas.cz](https://rapidoc.croapp.cz/).**

The *rapi* package is a library that queries the REST API available at <https://api.mujrozhlas.cz>. For example, this endpoint <https://api.mujrozhlas.cz/stations>, which returns the metadata of all stations in JSON form. The JSON is then converted to Python domain object for further work. This library therefore converts JSON into Python objects that can be directly used in Python code.

## Usage

```py
from rapi import Client

client = Client()
stations = client.get_stations()
for station in stations:
    print(station)
```

```json
{
  "uuid": "4082f63f-30e8-375d-a326-b32cf7d86e02",
  "title": "Český rozhlas Radiožurnál",
  "title_short": "Radiožurnál",
  "subtitle": "",
  "color": "#ED2E38",
  "code": "radiozurnal",
  "priority": 100,
  "span": "allover",
  "broadcast_name": "radiozurnal"
}
...
```

See examples more examples [here](https://czech-radio.github.io/rapi/).

## Installation

Install the lates package version from repository main branch.

```shell
python -m pip install git+https://github.com/czech-radio/rapi.git
```

## Documentation

See the published [documentation](https://czech-radio.githup.io/rapi) for more information.

You can build documentation localy with help of Sphinx. Be sure you have [Pandoc](https://pandoc.org/installing.html) installed and in the path. Go to `docs` folder in the project direcotry and build it with following command. The result is located in `docs/build` folder, open the `index.html` in your browser.

```shell
sphinx-build source build
```
