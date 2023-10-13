# from rapi.helpers._logger import log_stdout as logo
import logging
import sys
from typing import Union

import pandas as pd
import pytest

from rapi import _model
from rapi._client import Client
from rapi.config import _config, _params
from rapi.config._config import Config

# from rapi.config import Config
# from rapi.config._config import Config
from rapi.helpers import helpers

# lg = logging.getLogger("log_stdout")
# lg.setLevel(logging.DEBUG)


@pytest.fixture
def client():
    sys.argv = ["rapi", "-vv"]
    cfg = Config("rapi")
    cfg.cfg_runtime_set_defaults()
    _client = Client(cfg)
    assert _client
    return _client


sample_shows = [
    "9f36ee8f-73a7-3ed5-aafb-41210b7fb935",
    "92fade97-7f7f-3a5a-be2a-9cd0ec4e97c4",
    "48678000-b905-3b68-9b80-f4d20326f03b",
]

shows_with_schedule_episodes = [
    "c7374f41-ae14-3b5c-8c04-385e3241deb4",
    "004a2d7e-0429-39a3-bc4d-34a3775c3fec",
]

sample_radio_11_shows = [
    "c239aa59-bc78-3180-9b58-5c911846630d",
    "af62bd59-1e49-3dae-a68b-90b11f5d2ae6",
    "d88f0d67-6ba1-3ba5-8fea-01e41a614037",
    "1bb635cd-7e8d-3ee2-a226-7a4ed1703481",
    "63d91d32-e7cc-3e12-beb1-5378c4945ccb",
    "ca875c03-d58a-3d5b-a483-fdcb8d178db6",
    "9de06fed-3aad-34c2-85dd-5c78c018a8b9",
    "04ae61d9-b01a-3ab5-b389-99577bfc355b",
    "772701e9-bef2-38bf-9709-1ad69b227d59",
    "b51fb1c9-3126-3536-b880-cbcf8e6da9e4",
    "c7374f41-ae14-3b5c-8c04-385e3241deb4",
    "6950f239-d234-331b-b20e-2067b498ffb3",
    "6e0350d0-d9a7-3a27-8cd3-252a763f48ea",
    "5734245c-946d-3b10-9bfb-d295580f3752",
    "ed4623ee-2379-35af-af56-32c7644eed5c",
    "9e69ad1e-d1b4-3b51-bb34-1c4b90119f5c",
    "aaeb0f7c-371f-3114-aef7-9e07bd92ab08",
    "eea3bcb1-bb0c-39a2-856b-ebe82e6a1704",
    "e269785f-cff6-3e5a-bdc9-c33f4e3e984c",
    "73639267-69a4-3302-b461-5b08e10f090e",
    "276c3b16-1e33-302c-98f7-8b68e0782623",
    "686fab67-09df-3c7d-bac1-ddfc0ab9992a",
    "bcb42b61-7227-32a5-8371-fb582584116f",
    "1a8454bd-0751-39ff-b5e6-4bd8cd89c672",
    "98826987-3209-3d70-8fbe-0b5020ba1449",
    "c0e403a9-9dea-365b-96ff-545320a69b4e",
    "d152812c-5997-3cbb-8729-205c164bd789",
    "ee9948d3-a358-3a22-b9d2-fba99b441e28",
    "c8b55621-253f-3ae7-90c1-d7efca90528d",
    "3c4cd8b7-e45a-3f76-8f13-26e441d0def8",
    "00670b4b-d74d-32d8-aebf-e2c4b22678ff",
    "907bf24f-9bcf-3ea9-af9e-d98533093dad",
    "94913c5f-941a-3dbb-a8a9-51fd42b7872a",
    "aee3c53f-8e2f-3529-ab57-5eb90e704bc3",
    "2226c3be-7f0d-3c82-af47-0ec6abe992a8",
    "067b38a3-49c5-3358-b2be-3a2a8317d9cd",
    "db41a784-5efd-3974-8545-557085ba0bb2",
    "aba1a33f-8706-3559-a222-52754426147c",
    "8c88ace6-c8a8-3ed1-b51d-85bdccefe20e",
    "fa69549d-0be2-3b9c-abb1-3134397518ca",
    "d200d0b5-78d5-3cca-9052-834f13135225",
    "d390683e-b259-326f-9cac-92dd9be66d79",
    "2b17b3ab-2dfa-3e2b-92d5-bbb205fca8f7",
    "460e1258-f164-3c4e-87b5-e4737fa746f2",
    "e22d3ce6-e61c-3674-a481-2165e55130c7",
    "42feeb29-171d-3e08-965c-61e8a214bb54",
    "6d53be2a-43da-340b-be7f-5f9cfc4059b9",
    "703e572a-515d-3c31-8857-4e18b42d3b60",
    "ae782b41-453a-3d51-a852-935749361d0b",
    "739a46c7-35e3-336e-a7d5-08a20b7e7677",
    "816732b1-04cc-3f40-972a-ba16bf5a6eb1",
    "37830b29-65e6-36f9-8fdf-4869d32ce617",
    "3e974230-f3e3-335e-a6b4-a7162bfd256d",
    "d49ca459-e552-338e-a1ce-efc6076d026b",
    "bf751809-cbf1-3e43-93ee-8f4a6792ad59",
    "a828aaf9-bd1f-3429-90eb-cff7576199c1",
    "1de9abe8-b086-3f11-8a35-71ef7cad3de6",
    "8e483c21-6368-31a0-9392-b60c7c148142",
    "ee6095c0-33ac-3526-b8bf-df233af38211",
    "616c190f-90f0-39fa-ba42-a78b6b71d1c9",
    "aca91178-1318-3c9b-a766-bead1b693c5a",
    "1b9d2970-f1de-37da-9b71-ba7d62671299",
    "8b78c4da-20b6-31bc-aa9f-db5288851fdb",
    "810cc218-8c3a-3480-9da3-006e07dc0080",
    "68a55594-5d72-3a50-a20a-d5e904d684c9",
    "48678000-b905-3b68-9b80-f4d20326f03b",
    "e9c2642e-2062-3cd1-92eb-9c178c714f6c",
    "56010c25-119b-32b6-ab7c-42de790db86d",
    "ff206383-d36b-3162-a136-e8335dd71cad",
    "9f36ee8f-73a7-3ed5-aafb-41210b7fb935",
]

sample_shows_with_schedule = [
    10,
    13,
    17,
    22,
    23,
    25,
    26,
    32,
    33,
    34,
    40,
    44,
    46,
    51,
    52,
    53,
    57,
    58,
    64,
    65,
    66,
]

sample_persons = [
    "1cb35d9d-fb24-37ee-8993-9f74e57ab2c7",
    "7b9d1544-8aab-3730-8f0a-4d0b463322be",
    "c5b35399-08c6-3057-8145-c6aaaac76d4d",
    "fcb6babc-e5f6-3b30-b126-583885584454",
]

sample_episodes = [
    "014cf0cc-f797-32b6-9909-d87e02444212",
]


@pytest.mark.client
def test_class_attrs_by_anotation_dict_dates(client) -> None:
    id = shows_with_schedule_episodes[0]
    endp = "shows/" + id + "/schedule-episodes"
    data = client.get_endpoint_full_json(endp)
    es = _model.Episode_schedule
    ea = _model.episode_schedule_anotation
    res = helpers.class_attrs_by_anotation_dict(data[0], es, ea)
    assert res
    print(res)


@pytest.mark.client
def test_get_station(client) -> None:
    station = client.get_station(str(11))
    assert station


@pytest.mark.current
@pytest.mark.client
def test_get_stations(client) -> None:
    # NOTE: Number of stations seems to be rather dynamic in time: 27, 28, 33
    stations1 = list(client.get_stations())
    assert stations1
    stations2 = list(client.get_stations(10))
    assert stations2
    assert len(stations2) == len(stations1)


@pytest.mark.client
def test_get_station_shedule_day_flat(client) -> None:
    data = client.get_station_schedule_day_flat("2023-08-19")
    assert data
    # pdf = pd.DataFrame(data, columns=["station"])
    # print(len(pdf))
    # pdf.sort_values(by="since")


@pytest.mark.client
def test_get_station_shows(client) -> None:
    data = client.get_station_shows(str(11), 500)
    assert data


@pytest.mark.client
def test_get_show(client) -> None:
    data = client.get_show("9f36ee8f-73a7-3ed5-aafb-41210b7fb935", 500)
    assert data


@pytest.mark.client
def test_get_show_episodes(client) -> None:
    data = client.get_show_episodes("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
    # https://mujrozhlas.croapi.cz/shows/9f36ee8f-73a7-3ed5-aafb-41210b7fb935/episodes
    assert data


# @pytest.mark.current
@pytest.mark.client
def test_show_episodes_filter(client) -> None:
    data = client.show_episodes_filter(sample_shows[0])
    assert data
    data = client.show_episodes_filter(
        sample_shows[0],
        "2010",
    )
    assert data
    data1 = client.show_episodes_filter(
        sample_shows[0],
        "2014",
        "2014-12",
    )
    assert data1
    data2 = client.show_episodes_filter(
        sample_shows[0],
        "2014",
        "2015-12",
    )
    assert data2
    assert len(list(data1)) < len(list(data2))


@pytest.mark.client
def test_get_show_episodes_schedule(client) -> None:
    id = shows_with_schedule_episodes[0]
    data = client.get_show_episodes_schedule(id)
    assert data


@pytest.mark.client
def test_get_station_schedule_day_flat(client) -> None:
    data = client.get_station_schedule_day_flat("2023-09-11", "11")
    # NOTE: WTF I get error occasionally when I run len(list(data)), data is iterator
    datalist = list(data)
    assert datalist
    assert len(datalist) == 173
    # df = pd.DataFrame(data, columns=["station"])
    print(datalist)


@pytest.mark.client
def test_get_station_schedule_day(client) -> None:
    data = client.get_station_schedule_day("2023-09-11", "11")
    assert data
    assert len(list(data)) == 141
    # df = pd.DataFrame(data, columns=["station"])
    print(list(data))


@pytest.mark.client
def test_get_schedule(client) -> None:
    data1 = client.get_schedule("2023-09-17", "2023-09-18")
    assert data1

    data2 = client.get_schedule("2023-09-17T8:00", "2023-09-17T9:00")
    assert data2

    data3 = client.get_schedule("2023-09-17T8:00", "2023-09-17T9:00", "11")
    assert len(list(data1)) > len(list(data2)) > len(list(data3))


@pytest.mark.client
def test_get_show_participants(client) -> None:
    sp = sample_shows_with_schedule[0]
    show_id = sample_radio_11_shows[sp]
    data = client.get_show_participants(show_id)
    assert data


@pytest.mark.client
def test_get_show_participants_with_roles(client) -> None:
    sp = sample_shows_with_schedule[0]
    show_id = sample_radio_11_shows[sp]
    data = client.get_show_participants_with_roles(show_id)
    assert data


@pytest.mark.client
def test_get_show_moderators(client) -> None:
    sp = sample_shows_with_schedule[0]
    show_id = sample_radio_11_shows[sp]
    data = client.get_show_moderators(show_id)
    assert data


@pytest.mark.client
def test_get_person(client) -> None:
    data = client.get_person(sample_persons[0])
    assert data
