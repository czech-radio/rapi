#!/bin/bash

declare -a urls=(
  "stations-all"
  "stations"
)
# curl -g -X GET "https://rapidev.croapp.cz/stations-all" | jq '.' > stations-all.json
dir='./runtime/rapidev_responses/'
for i in "${urls[@]}"; do
  curl -g -X GET "https://rapidev.croapp.cz/${i}" | jq '.' > "${dir}/${i}.json"
done

