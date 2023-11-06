"""
The integration test for the client.

Please think about about tets names twice!
Test names should be descriptive and describe the feature/intent.
Don't copy the method names blindly. Thanks and happy coding.
"""

import pandas as pd
import pytest

from rapi import Client, Show, Station


@pytest.fixture
def client():
    """Make a default client instance."""
    return Client()


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

# ########################################################################### #
# Stations
# ########################################################################### #


# @pytest.mark.client
# def test_that_available_stations_are_retrieved(client) -> None:
#     result = list(client.get_stations())
#     assert len(result) > 10


# @pytest.mark.client
# def test_that_available_stations_are_retrieved_with_limit(client) -> None:
#     result = list(client.get_stations(limit=10))
#     assert len(result) == 10


@pytest.mark.client
def test_that_station_is_retrived(client) -> None:
    result = client.get_station(station_id=11)
    assert isinstance(result, Station) and result.title_short == "Radiožurnál"


# @pytest.mark.client
# def test_class_attrs_by_anotation_dict_dates(client) -> None:
#     show_id = shows_with_schedule_episodes[0]
#     endp = "shows/" + show_id + "/schedule-episodes"
#     result = client._get_endpoint_data(endp)
#     result1 = _shared.class_attrs_by_anotation_dict(result[0], _domain.ScheduledEpisode)
#     assert result1


# @pytest.mark.client
# def test_get_station_shedule_day_flat(client) -> None:
#     result = client.get_station_schedule_day_flat("2023-08-19")
#     assert result

# ########################################################################### #
# Shows
# ########################################################################### #

# @pytest.mark.client
# def test_that_all_shows_are_retrived(client) -> None:
#     result = client.get_shows(str(11))
#     assert len(list(result)) > 10


# @pytest.mark.client
# def test_that_shows_are_retrived_with_limit(client) -> None:
#     result = client.get_shows(str(11), limit=10)
#     assert len(list(result)) == 10


@pytest.mark.client
def test_that_show_is_retrieved(client) -> None:
    result = client.get_show(show_id="9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
    assert isinstance(result, Show) and len(result.title) > 0


# ########################################################################### #
# Episodes
# ########################################################################### #


@pytest.mark.client
def test_get_show_episodes(client) -> None:
    result = client.get_show_episodes("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
    print(list(result))
    assert result


# @pytest.mark.client
# def test_show_episodes_filter(client) -> None:
#     result = list(client.get_show_episodes_filter(sample_shows[0]))
#     assert len(result) > 0


# @pytest.mark.client
# def test_get_show_episodes_schedule(client) -> None:
#     show_id = shows_with_schedule_episodes[0]
#     result = client.get_show_episodes_schedule(show_id)
#     assert result


# @pytest.mark.client
# def test_get_station_schedule_day_flat(client) -> None:
#     result = client.get_station_schedule_day_flat("2023-09-11", "11")
#     result1 = list(result)
#     assert len(result1) > 0
#     result2 = pd.DataFrame(result1, columns=["station"])
#     assert len(result2) > 0


# @pytest.mark.client
# def test_get_station_schedule_day(client) -> None:
#     result = client.get_station_schedule_day("2023-09-11", "11")
#     assert result
#     result1 = list(result)
#     assert len(result1) == 141
#     result2 = pd.DataFrame(result1, columns=["station"])
#     assert len(result2) > 0


# @pytest.mark.client
# def test_get_schedule(client) -> None:
#     show = "2226c3be-7f0d-3c82-af47-0ec6abe992a8"
#     station = "4082f63f-30e8-375d-a326-b32cf7d86e02"

#     result = list(client.get_schedule(show))
#     assert len(result) > 0
#     result1 = list(client.get_schedule(show, station))
#     assert len(result1) > 0
#     result2 = list(client.get_schedule(show, station, "2023-10-01"))
#     assert len(result2) > 0
#     result3 = list(client.get_schedule(show, station, "2023-10-20", "2023-10-21"))
#     assert len(result3) > 0


# @pytest.mark.client
# def test_get_schedule_by_date(client) -> None:
#     result1 = list(client.get_schedule_by_date("2023-09-17", "2023-09-18"))
#     assert result1

#     result2 = list(client.get_schedule_by_date("2023-09-17T8:00", "2023-09-17T9:00"))
#     assert result2

#     result3 = list(
#         client.get_schedule_by_date("2023-09-17T8:00", "2023-09-17T9:00", "11")
#     )
#     assert len(result1) > len(result2) > len(result3)


# @pytest.mark.client
# def test_get_show_participants(client) -> None:
#     sp = sample_shows_with_schedule[0]
#     show_id = sample_radio_11_shows[sp]
#     result = list(client.get_show_participants(show_id))
#     assert len(result) > 0


# @pytest.mark.client
# def test_get_show_participants_with_roles(client) -> None:
#     sp = sample_shows_with_schedule[0]
#     show_id = sample_radio_11_shows[sp]
#     result = list(client.get_show_participants_with_roles(show_id))
#     assert len(result) > 0


# @pytest.mark.client
# def test_get_show_moderators(client) -> None:
#     sp = sample_shows_with_schedule[0]
#     show_id = sample_radio_11_shows[sp]
#     result = list(client.get_show_moderators(show_id))
#     assert len(result) > 0


# @pytest.mark.client
# def test_get_person(client) -> None:
#     result = client.get_person(sample_persons[0])
#     assert result
