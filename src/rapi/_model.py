"""
FIXME
"""

import datetime
import datetime as dt
import json
from dataclasses import asdict, dataclass


def str_pretty_json(cls):
    """
    __srt__ method for datalass which prints dataclass as formated json. dataclass field values must be compatible with json requirements
    """

    def __str__(self):
        df = json.dumps(
            asdict(self),
            indent=2,
            ensure_ascii=False,
            cls=DatetimeEncoder,
        )
        return df

    cls.__str__ = __str__
    return cls


class DatetimeEncoder(json.JSONEncoder):
    """format json datetime value when duming the json"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


@dataclass
@str_pretty_json
class StationIDs:
    # OPENMEDIA:
    # src: [https://github.com/czech-radio/organization/blob/main/analytics/reporting/specification.md#stanice]
    openmedia_id: str = "openmedia_id"
    # exmp: 11
    openmedia_stanice: str = "openmedia_stanice"
    # exmp: RZ-Radiožurnál

    # CROAPP
    # src: [https://rapidev.croapp.cz/stations]
    croapp_code: str = "croapp_code"
    # exmp.: "radiozurnal"
    croapp_stitle: str = "croapp_shortTitle"
    # exmp.: "Radiožurnál"
    croapp_guid: str = "croapp_id"
    # exmp.: "4082f63f-30e8-375d-a326-b32cf7d86e02"


@dataclass(frozen=True)
@str_pretty_json
class Station:
    uuid: str
    title: str
    title_short: str
    subtitle: str
    color: str
    code: str
    priority: int
    span: str
    broadcast_name: str


station_anotation: dict = {
    "uuid": {"json": "id"},
    "title": {"json": "attributes.title"},
    "title_short": {"json": "attributes.shortTitle"},
    "subtitle": {"json": "attributes.subtitle"},
    "color": {"json": "attributes.color"},
    "code": {"json": "attributes.code"},
    "priority": {"json": "attributes.priority"},
    "span": {"json": "attributes.stationType"},
    "broadcast_name": {"json": "meta.ga.siteBroadcastStation"},
}


@dataclass(frozen=True)
@str_pretty_json
class Show:
    uuid: str
    type: str
    content: bool
    title: bool
    active: bool
    aired: bool
    podcast: bool
    priority: int
    child_friendly: bool
    description: str
    description_short: str
    updated: dt.datetime


show_anotation: dict = {
    "uuid": {"json": "id"},
    "type": {"json": "attributes.showType"},
    "content": {"json": "attributes.showContent"},
    "title": {"json": "attributes.title"},
    "active": {"json": "attributes.active"},
    "aired": {"json": "attributes.aired"},
    "podcast": {"json": "attributes.podcast"},
    "priority": {"json": "attributes.priority"},
    "child_friendly": {"json": "attributes.childFriendly"},
    "description": {"json": "attributes.description"},
    "description_short": {"json": "attributes.shortDescription"},
    "updated": {"json": "attributes.updated"},
}


@dataclass(frozen=True)
@str_pretty_json
class Episode:
    uuid: str
    title: str
    title_short: str
    description: str
    since: dt.datetime
    till: dt.datetime
    updated: dt.datetime
    part: str
    title_mirrored: str
    content_creator: str
    content_id: str
    base_id: str


episode_anotation: dict = {
    "uuid": {"json": "id"},
    "title": {"json": "attributes.title"},
    "title_short": {"json": "attributes.shortTitle"},
    "description": {"json": "attributes.description"},
    "since": {"json": "attributes.since"},
    "till": {"json": "attributes.till"},
    "updated": {"json": "attributes.updated"},
    "part": {"json": "attributes.part"},
    "title_mirrored": {"json": "attributes.mirroredShow.title"},
    "content_creator": {"json": "meta.ga.contentCreator"},
    "content_id": {"json": "meta.ga.contentId"},
    "base_id": {"json": "meta.ga.baseId"},
}


@dataclass(frozen=True)
@str_pretty_json
class Episode_schedule:
    uuid: str
    title: str
    description: str
    station: str
    station_code: int
    show_priority: int
    show_times: str
    since: dt.datetime
    till: dt.datetime


episode_schedule_anotation: dict = {
    "uuid": {"json": "id"},
    "title": {"json": "attributes.title"},
    "description": {"json": "attributes.description"},
    "station": {"json": "relationships.station.data.id"},
    "station_code": {"json": "attributes.station_code"},
    "show_priority": {"json": "attributes.showPriority"},
    "show_times": {"json": "attributes.showTimes"},
    "since": {"json": "attributes.since"},
    "till": {"json": "attributes.till"},
}


@dataclass
@str_pretty_json
class Person:
    uuid: str
    title: str
    description_short: str
    description: str
    profile_id: str
    role: str
    participation_link: str
    participation_data: str


person_anotation: dict = {
    "uuid": {"json": "id"},
    "title": {"json": "attributes.title"},
    "description_short": {"json": "attributes.short_description"},
    "description": {"json": "attributes.description"},
    "profile_id": {"json": "attributes.profile_id"},
    "role": {"json": "meta.role"},
    "participation_link": {
        "json": "relationships.participation.links.related"
    },
    "participation_data": {"json": "relationships.participation.data"},
}
