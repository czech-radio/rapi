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
    id: str = ""
    show_type: str = ""
    show_content: bool = False
    title: bool = False
    active: bool = False
    aired: bool = False
    podcast: bool = False
    priority: int = 0
    child_friendly: bool = False
    description: str = ""
    short_description: str = ""


show_anotation: dict = {
    "uuid": {"json": "id"},
    "span": {"json": "showType"},
}


@dataclass
@str_pretty_json
class Episode:
    id: str = ""
    title: str = ""
    short_title: str = ""
    description: str = ""
    since: dt.datetime = dt.datetime(1, 1, 1, 0, 0)
    till: dt.datetime = dt.datetime(1, 1, 1, 0, 0)
    updated: dt.datetime = dt.datetime(1, 1, 1, 0, 0)
    mirrored_show_title: str = ""


class Schedule:
    pass
