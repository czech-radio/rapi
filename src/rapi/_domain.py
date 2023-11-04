"""
This module contains domain models and functions.
"""

import datetime
import json
from dataclasses import asdict, dataclass
from typing import Any, ClassVar, Protocol


def output_json(cls):
    """
    Modify :py:method:`__str__` method of a dataclass to output JSON.
    """

    def __str__(self):
        result = json.dumps(
            asdict(self),
            indent=2,
            ensure_ascii=False,
            cls=DatetimeEncoder,
        )
        return result

    cls.__str__ = __str__

    return cls


class DatetimeEncoder(json.JSONEncoder):
    """
    Format the datetime value to conform to ISO 8601.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


class Anotated(Protocol):
    """
    This type contains annotation class variable used for JSON export.
    """

    anotation: dict[str, Any]


@dataclass(frozen=True, slots=True)
@output_json
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

    anotation: ClassVar[dict[str, dict]] = {
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


@dataclass(frozen=True, slots=True)
@output_json
class Show:
    """
    FIXME
    """

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
    updated: datetime.datetime

    anotation: ClassVar[dict[str, dict]] = {
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
@output_json
class Episode:
    """
    FIXME
    """

    uuid: str
    title: str
    title_short: str
    description: str
    since: datetime.datetime
    till: datetime.datetime
    updated: datetime.datetime
    part: str
    title_mirrored: str
    content_creator: str
    content_id: str
    base_id: str

    anotation: ClassVar[dict[str, dict]] = {
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
@output_json
class ScheduledEpisode:
    """
    FIXME
    """

    uuid: str
    title: str
    description: str
    station: str
    station_code: int
    show_priority: int
    show_times: str
    since: datetime.datetime
    till: datetime.datetime

    anotation: ClassVar[dict[str, dict]] = {
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
@output_json
class Person:
    """
    FIXME
    """

    uuid: str
    title: str
    description_short: str
    description: str
    profile_id: str
    role: str
    participation_link: str
    participation_data: str

    anotation: ClassVar[dict[str, dict]] = {
        "uuid": {"json": "id"},
        "title": {"json": "attributes.title"},
        "description_short": {"json": "attributes.short_description"},
        "description": {"json": "attributes.description"},
        "profile_id": {"json": "attributes.profile_id"},
        "role": {"json": "meta.role"},
        "participation_link": {"json": "relationships.participation.links.related"},
        "participation_data": {"json": "relationships.participation.data"},
    }
