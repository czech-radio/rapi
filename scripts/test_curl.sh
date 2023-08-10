#!/bin/bash
url="https://rapidev.croapp.cz"
# part="shows"
part="stations"
limit="?page%5Blimit%5D=100"
url_whole="${url}/${part}${limit}"
# curl -g -X GET "${url_whole}" -H "accept: application/vnd.api+json" | jq '.'

par="radiozurnal"

# declare -a ids=(
# )

curl -X GET "https://rapidev.croapp.cz/schedule-day?station=$par" -H  "accept: application/vnd.api+json"$ | jq -R '.'
