import datetime as dt
import json
from dataclasses import asdict, dataclass
from typing import Type, TypeVar

from rapi._helpers import DatetimeEncoder


def str_pretty_json(cls):
    def __str__(self):
        df = json.dumps(
            asdict(self), indent=2, ensure_ascii=False, cls=DatetimeEncoder
        )
        return df

    cls.__str__ = __str__
    return cls


@dataclass
@str_pretty_json
class StationIDs:
    ### OPENMEDIA:
    #### src: [https://github.com/czech-radio/organization/blob/main/analytics/reporting/specification.md#stanice]
    openmedia_id: str = "openmedia_id"
    ##### exmp: 11
    openmedia_stanice: str = "openmedia_stanice"
    ##### exmp: RZ-Radiožurnál

    ### CROAPP
    #### src: [https://rapidev.croapp.cz/stations]
    croapp_code: str = "croapp_code"
    ##### exmp.: "radiozurnal"
    croapp_stitle: str = "croapp_shortTitle"
    ##### exmp.: "Radiožurnál"
    croapp_guid: str = "croapp_id"
    ##### exmp.: "4082f63f-30e8-375d-a326-b32cf7d86e02"


@dataclass
@str_pretty_json
class Station:
    uuid: str = ""
    title: str = ""
    title_short: str = ""
    subtitle: str = ""
    color: str = ""
    code: str = ""
    priority: int = 0
    span: str = ""
    broadcast_name: str = ""


# station_anotation: dict = {
# "uuid": {"json": ["attributes","id"]},
# "title": {"json": ["attributes","title"]},
# "title_short": {"json": ["attributes","shortTitle"]},
# "subtitle": {"json": ["attributes","subtitle"]},
# "color": {"json": ["attributes","color"]},
# "code": {"json": ["attributes","code"]},
# "priority": {"json": ["attributes","priority"]},
# "span": {"json": ["attributes","stationType"]},
# "broadcast_name": {"json": ["meta","ga","siteBroadcastStation"]},
# }

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


@dataclass
@str_pretty_json
class Show:
    uuid: str = ""
    type: str = ""
    content: bool = False
    title: bool = False
    active: bool = False
    aired: bool = False
    podcast: bool = False
    priority: int = 0
    child_friendly: bool = False
    description: str = ""
    description_short: str = ""
    updated: dt.datetime = dt.datetime(1, 1, 1, 0, 0)


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


@dataclass
@str_pretty_json
class Episode:
    uuid: str = ""
    title: str = ""
    title_short: str = ""
    description: str = ""
    since: dt.datetime = dt.datetime(1, 1, 1, 0, 0)
    till: dt.datetime = dt.datetime(1, 1, 1, 0, 0)
    updated: dt.datetime = dt.datetime(1, 1, 1, 0, 0)
    part: str = ""
    title_mirrored: str = ""
    content_creator: str = ""
    content_id: str = ""
    base_id: str = ""


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


class Schedule:
    pass
