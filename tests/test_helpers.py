from typing import Union

from rapi import helpers
from rapi.helpers import analyze as an
from rapi.helpers import pprint as pp
from rapi.helpers import ptype as pt

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


def test_dict_get_path() -> None:
    val = helpers.dict_get_path(nested_dict, ["person1", "name"])
    assert val == "John Doe"
    val = helpers.dict_get_path(nested_dict, ["person1", "contact", "email"])
    assert val == "john@example.com"


def test_deep_merge_dicts():
    dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
    dict2 = {"b": {"y": "ahoj", "z": 40}, "c": 3}
    merged_dict = helpers.deep_merge_dicts(dict1, dict2)
    print(merged_dict)


def test_dict_paths_vectors() -> None:
    print()
    res = helpers.dict_paths_vectors(nested_dict)
    print(res)


def test_request_url() -> None:
    print()
    url = "https://rapidev.croapp.cz/stations?"
    # url = "https://rapidoc.croapp.cz/apifile/openapi.yaml"
    # url = "https://rapidev.croapp.cz/stat?"
    req = helpers.request_url(url)
    helpers.ptype(req.headers)
    helpers.pprint(dict(req.headers))
    print(req.status_code)
    print(req.reason)


def test_request_url_json() -> None:
    print()
    url = "https://rapidev.croapp.cz/stations?"
    # url = "https://rapidoc.croapp.cz/apifile/openapi.yaml"
    jdata = helpers.request_url_json(url)
    assert jdata
    an(jdata)
    pp(jdata)
