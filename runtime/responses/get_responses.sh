#!/bin/bash

declare -a urls=(
  "stations-all"
  "stations"
)
# curl -g -X GET "https://rapidev.croapp.cz/stations-all" | jq '.' > stations-all.json
for i in "${urls[@]}"; do
  curl -g -X GET "https://rapidev.croapp.cz/${i}" | jq '.' > "${i}.json"
done

