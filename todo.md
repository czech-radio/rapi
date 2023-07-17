# Parsing schema
url="https://rapidoc.croapp.cz/apifile/openapi.yaml"

## Issues
- the api may change in future
- considering dynamic parsing
- there are currently 3 parsers:
	- swagger-parser
	- openapi-parser
	- openapi3-parser

- I was not able to parse the schema successfully with any of the parsers

- swagger_parser gives error:
Object at "/components/schemas" does not contain key: timeGroupItem_relationships'
- it means there is missing definition for timeGroupItem_relationship. It is only referenced in schema.
- will try adding dummy variable definition

##
