# Issues
## automatic schema parsing
url="https://rapidoc.croapp.cz/apifile/openapi.yaml"
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

## stations IDs
- added ./data/stations_ids_table.csv
- compiled table from:
a) https://github.com/czech-radio/organization/blob/main/analytics/reporting/specification.md#stanice
b) https://rapidoc.croapp.cz/stations-all

- missing or incompatible data for some stations
- the compiled table should be checked by someone else


