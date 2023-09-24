import os
import re
from typing import Union

import pytest

from rapi.helpers import helpers

simple_dict_list = [
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Jane", "age": 25, "city": "Los Angeles"},
    {"name": "Michael", "age": 40, "city": "Chicago"},
    {"name": "Emily", "age": 22, "city": "San Francisco"},
]

nested_dict = {
    "dummy": "hello_dumm",
    "person1": {
        "name": "John Doe",
        "age": 30,
        "contact": {"email": "john@example.com", "phone": "123-456-7890"},
    },
    "person2": {
        "name": "Jane Smith",
        "age": 25,
        "contact": {"email": "jane@example.com", "phone": "987-654-3210"},
    },
    "dummy2": "hello_dumm",
}


@pytest.mark.helpers
def test_dict_get_path() -> None:
    val = helpers.dict_get_path(nested_dict, ["person1", "name"])
    assert val == "John Doe"
    val = helpers.dict_get_path(nested_dict, ["person1", "contact", "email"])
    assert val == "john@example.com"


@pytest.mark.helpers
def test_deep_merge_dicts():
    dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
    dict2 = {"b": {"y": "ahoj", "z": 40}, "c": 3}
    merged_dict = helpers.deep_merge_dicts(dict1, dict2)
    assert merged_dict
    print(merged_dict)


@pytest.mark.helpers
def test_dict_paths_vectors() -> None:
    res = helpers.dict_paths_vectors(nested_dict, list())
    assert res
    print(res)


@pytest.mark.helpers
def test_request_url() -> None:
    print()
    url = "https://rapidev.croapp.cz/stations?"
    # url = "https://rapidev.croapp.cz/stat?"
    req = helpers.request_url(url)
    assert req is not None
    helpers.pt(req.headers)
    helpers.pp(dict(req.headers))
    print(req.status_code)
    print(req.reason)


@pytest.mark.helpers
def test_extract_link_path():
    print()
    url = "stations/4082f63f-30e8-375d-a326-b32cf7d86e02/shows"
    out = re.sub(r"[^/]+/", "", url)
    assert out
    print(out)


@pytest.mark.helpers
def test_request_url_json() -> None:
    print()
    url = "https://rapidev.croapp.cz/stations?"
    # url="https://rapidev.croapp.cz/stations?page[1]=0&page[limit]=1"
    jdata = helpers.request_url_json(url)
    assert jdata
    print(jdata)


@pytest.mark.helpers
def test_request_url_yaml() -> None:
    ### urls:
    # https://rapidoc.croapp.cz/index.html ->
    url = "https://rapidoc.croapp.cz/apifile/openapi.yaml"
    ydata = helpers.request_url_yaml(url)
    assert ydata
    helpers.pp(ydata)


@pytest.mark.helpers
def test_current_timezone() -> None:
    tz = helpers.current_timezone()
    assert tz
    print(tz)


@pytest.mark.helpers
def test_datenow_with_timezone() -> None:
    dt = helpers.datenow_with_timezone()
    assert dt


sample_dates = [
    "2023",
    "2023-09",
    "2023-09-11",
    "2023-09-12T00:00+03:00",
    "2023-01-09T10",
    "2023-01-09T10",
    "2023-01-09T10:11",
    "2023-01-09T10:11",
    "2023-01-09T10:11:39",
    "2023-01-09T10:13:10+01:00",
    "2023-01-09T10:13:10+08:00",
    "2023-01-09T10:13:10+10:00",
    "2023-01-09T10:13:10+11:00",
]


@pytest.mark.helpers
def test_parse_date_regex() -> None:
    print()
    for d in sample_dates:
        dt = helpers.parse_date_regex(d)
        assert dt
        print(dt)


@pytest.mark.helpers
def test_parse_date_optional_fields() -> None:
    print()
    sd = sample_dates
    _func = helpers.parse_date_optional_fields
    for d in sd:
        dt = _func(d)
        print(dt)
    dt1 = _func(sd[-1])
    dt2 = _func(sd[-2])
    assert dt1 < dt2
    print(dt2 - dt1)


@pytest.mark.helpers
def test_filepath_to_vector() -> None:
    cwd = os.getcwd()
    fp = os.path.join(cwd, "kek.txt")
    vec = helpers.filepath_to_vector(fp)
    assert vec
    print(vec)
