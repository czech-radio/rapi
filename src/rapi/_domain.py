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
    """
    The station e.g. 'Plus', see <https://plus.rozhlas.cz/>.
    """

    uuid: str
    title: str
    title_short: str
    subtitle: str
    color: str  # The color in hexadecimal notation e.g. '#abcdef'
    code: str
    priority: int
    span: str
    broadcast_name: str

    # The path of the retrieved JSON field.
    anotation: ClassVar[dict[str, str]] = {
        "uuid": "id",
        "title": "attributes.title",
        "title_short": "attributes.shortTitle",
        "subtitle": "attributes.subtitle",
        "color": "attributes.color",
        "code": "attributes.code",
        "priority": "attributes.priority",
        "span": "attributes.stationType",
        "broadcast_name": "meta.ga.siteBroadcastStation",
    }


@dataclass(frozen=True, slots=True)
@output_json
class Show:
    """
    The aired show e.g 'Pro a proti', see <https://plus.rozhlas.cz/pro-a-proti-6482952>.
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

    # The mapping between class attribute and possibly nested JSON field.
    anotation: ClassVar[dict[str, str]] = {
        "uuid": "id",
        "type": "attributes.showType",
        "content": "attributes.showContent",
        "title": "attributes.title",
        "active": "attributes.active",
        "aired": "attributes.aired",
        "podcast": "attributes.podcast",
        "priority": "attributes.priority",
        "child_friendly": "attributes.childFriendly",
        "description": "attributes.description",
        "description_short": "attributes.shortDescription",
        "updated": "attributes.updated",
    }


@dataclass(frozen=True)
@output_json
class Episode:
    """
    The episode of show e.g. <https://shorturl.at/zGHUV>.
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

    # The mapping between class attribute and possibly nested JSON field.
    anotation: ClassVar[dict[str, str]] = {
        "uuid": "id",
        "title": "attributes.title",
        "title_short": "attributes.shortTitle",
        "description": "attributes.description",
        "since": "attributes.since",
        "till": "attributes.till",
        "updated": "attributes.updated",
        "part": "attributes.part",
        "title_mirrored": "attributes.mirroredShow.title",
        "content_creator": "meta.ga.contentCreator",
        "content_id": "meta.ga.contentId",
        "base_id": "meta.ga.baseId",
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

    anotation: ClassVar[dict[str, str]] = {
        "uuid": "id",
        "title": "attributes.title",
        "description": "attributes.description",
        "station": "relationships.station.data.id",
        "station_code": "attributes.station_code",
        "show_priority": "attributes.showPriority",
        "show_times": "attributes.showTimes",
        "since": "attributes.since",
        "till": "attributes.till",
    }


@dataclass
@output_json
class Person:
    """
    A respondent or  moderator appearing in an episode.
    """

    uuid: str
    title: str
    description: str
    description_short: str
    profile_id: str
    role: str
    participation_link: str
    participation_data: str

    anotation: ClassVar[dict[str, str]] = {
        "uuid": "id",
        "title": "attributes.title",
        "description_short": "attributes.short_description",
        "description": "attributes.description",
        "profile_id": "attributes.profile_id",
        "role": "meta.role",
        "participation_link": "relationships.participation.links.related",
        "participation_data": "relationships.participation.data",
    }
