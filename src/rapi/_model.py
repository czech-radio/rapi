from dataclasses import asdict, dataclass


@dataclass
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
class Station:
    id: str = ""
    title: str = ""
    short_title: str = ""
    subtitle: str = ""
    color: str = ""
    code: str = ""
    priority: int = 0
    station_type: str = ""


@dataclass
class Show:
    id: str = ""
    showType: str = ""
    showContent: bool = False
    title: bool = False
    active: bool = False
    aired: bool = False
    podcast: bool = False
    priority: int = 0
    childFriendly: bool = False
    description: str = ""
    shortDescription: str = ""


@dataclass
class Episode:
    id: str = ""
    title: str = ""
    shortTitle: str = ""
    description: str = ""
    since: str = ""
    till: str = ""
    mirroredShow_title: str = ""


class Schedule:
    pass
