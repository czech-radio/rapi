# Issues

## Automatic schema parsing

url="<https://rapidoc.croapp.cz/apifile/openapi.yaml>"

- the api may change in future
- considering dynamic parsing
- there are currently 3 parsers:
  - swagger-parser
  - openapi-parser
  - openapi3-parser

- I was unable to parse the schema successfully with any of the parsers

- swagger_parser gives error:
Object at "/components/schemas" does not contain key: timeGroupItem_relationships'
- it means there is missing definition for timeGroupItem_relationship. It is only referenced in schema.
- will try adding dummy variable definition

## Stations IDs

- added ./data/stations_ids_table.csv
- compiled table from:
a) <https://github.com/czech-radio/organization/blob/main/analytics/reporting/specification.md#stanice>
b) <https://rapidoc.croapp.cz/stations-all>

- missing or incompatible data for some stations
- the compiled table should be checked by someone else

## src/rapi/__init__.py

**DL (resolved): You must place `py.typed` to the package root diretory.**

-there is problem using mypy.
-importing __version__ from __init__.py to use it in command.py to print version results in error:

src/rapi/command.py:9: error: Skipping analyzing "rapi.__init__": module is installed, but missing library stubs or py.typed marker  [import]
src/rapi/command.py:9: note: See <https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports>

-without iporting __version__ checking with mypy is susccesful

-will have to find another way automatic versioning using "single point of truth" to update: git tag, projcet.toml version, hardcoded version in code, version in README.md
