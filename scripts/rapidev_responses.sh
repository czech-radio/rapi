#!/bin/bash
scriptpath="${BASH_SOURCE[0]:-$0}"
scriptdir="${scriptpath%/*}"
if [[ "$scriptdir" == "." ]] ; then
  repodir=".."
else
  repodir="."
fi

dstdir_reply_all="${repodir}/runtime/rapidev_reply_all"
dstdir_reply_samples="${repodir}/runtime/rapidev_reply_samples"

api_doc='https://rapidoc.croapp.cz'
api_dev='https://rapidev.croapp.cz'

declare -a url_all_sublinks=(
  "stations-all"
  "stations"
  "shows"
  "serials"
  "schedule"
  "program"
  "schedule-day"
  "schedule-day-flat"
  "schedule-current"
  "episodes"
  "genres"
  "persons"
  "topics"
  "keywords"
)

GetUrl(){
 local url_part="$1"
 local url_whole="${api_dev}/${url_part}"
 curl -g -X GET "${url_whole}" -H "accept: application/vnd.api+json"
}

GetAll(){
  for i in "${url_all_sublinks[@]}"; do
    local url_part="$i"
    local url_whole="${api_dev}/${url_part}"
    echo "DOWNLOADING: ${url_whole}"
    echo "DST: ${dstdir_reply_all}"

    # dstdir_reply_all="$(realpath "${dstdir_reply_all}")"
    if [[ ! -d "$dstdir_reply_all" ]]; then
      echo creating directory "$dstdir_reply_all"
      mkdir "$dstdir_reply_all"
    fi

    curl -g -X GET "${url_whole}" -H "accept: application/vnd.api+json" | jq '.' > "${dstdir_reply_all}/${url_part}.json"
    echo
  done
}

# x-object-type
### type: station
sample_station="4082f63f-30e8-375d-a326-b32cf7d86e02"
### type: show
sample_show="c239aa59-bc78-3180-9b58-5c911846630d"
### type: scheduleEpisode
sample_schedule="000448e3-99f1-3aac-bac2-edf3be93647d"
### type: episode
sample_episode="000006c7-4204-33fe-897c-3765247637a5"
### type: person
sample_person="8bed7519-4284-32e5-a693-15144f7edc6d"
### type: topic
sample_topic="fdb37f89-29c9-4faf-be29-e867def891cb"
### type: keyword
sample_keyword="9c605442-9185-3f4f-b6c5-6b2c0bb1bcb7"

declare -a url_sample_sublinks=( 
  "stations/${sample_station}"
  "stations/${sample_station}/shows"
  "stations/${sample_station}/participants"
  "shows/${sample_show}"
  "shows/${sample_show}/episodes"
  "shows/${sample_show}/serials"
  "shows/${sample_show}/participants"
  "shows/${sample_show}/schedule-episodes"
  "schedule/${sample_schedule}"
  "episodes/${sample_episode}"
  "episodes/${sample_episode}/keywords"
  "episodes/${sample_episode}/genres"
  "persons/${sample_person}"
  "persons/${sample_person}/participation"
  "topics/${sample_topic}"
  "topics/${sample_topic}/episodes"
  "keywords/${sample_keyword}"
)

GetSamples(){
  # set -x
  for i in "${url_sample_sublinks[@]}"; do
    echo
    echo "${i^^}"
    local url_part="$i"
    local url_whole="${api_dev}/${url_part}"
    local url_main="${url_part%%/*}"
    local rem="${url_part#*/}"
    local id=${rem%/*}
    local url_sub="${rem#*/}"

    local dstmain="${dstdir_reply_samples}/${url_main}"
    local dstid="${dstmain}/${id}"

    ### Create directories
    if [[ ! -d "${dstdir_reply_samples}" ]]; then
      echo creating directory "$dstdir"
      mkdir "$dstdir_reply_samples"
    fi
    if [[ ! -d "$dstmain" ]]; then
      echo creating directory "$dstmain"
      mkdir "$dstmain"
    fi
    if [[ ! -d "$dstid" ]]; then
      echo creating directory "$dstid"
      mkdir "$dstid"
    fi
    
    ### Download files
    dstfile="${dstid}/${url_sub}.json"
    curl -g -X GET "${url_whole}" \
      -H "accept: application/vnd.api+json" \
      | jq '.' >  "${dstfile}"
  done
}

"$@"

