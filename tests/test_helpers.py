import re
from typing import Union

from rapi import _helpers

# data = [
# {'name': 'John', 'age': 30, 'city': 'New York'},
# {'name': 'Jane', 'age': 25, 'city': 'Los Angeles'},
# {'name': 'Michael', 'age': 40, 'city': 'Chicago'},
# {'name': 'Emily', 'age': 22, 'city': 'San Francisco'}
# ]

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
    val = _helpers.dict_get_path(nested_dict, ["person1", "name"])
    assert val == "John Doe"
    val = _helpers.dict_get_path(nested_dict, ["person1", "contact", "email"])
    assert val == "john@example.com"


def test_deep_merge_dicts():
    dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
    dict2 = {"b": {"y": "ahoj", "z": 40}, "c": 3}
    merged_dict = _helpers.deep_merge_dicts(dict1, dict2)
    print(merged_dict)


def test_dict_paths_vectors() -> None:
    print()
    res = _helpers.dict_paths_vectors(nested_dict, list())
    print(res)


def test_request_url() -> None:
    print()
    url = "https://rapidev.croapp.cz/stations?"
    # url = "https://rapidev.croapp.cz/stat?"
    req = _helpers.request_url(url)
    assert req is not None
    _helpers.pt(req.headers)
    _helpers.pp(dict(req.headers))
    print(req.status_code)
    print(req.reason)


def test_extract_link_path():
    print()
    url = "stations/4082f63f-30e8-375d-a326-b32cf7d86e02/shows"
    out = re.sub(r"[^/]+/", "", url)
    print(out)


def test_request_url_json() -> None:
    print()
    url = "https://rapidev.croapp.cz/stations?"
    # url="https://rapidev.croapp.cz/stations?page[1]=0&page[limit]=1"
    jdata = _helpers.request_url_json(url)
    assert jdata


def test_request_url_yaml() -> None:
    ### urls:
    # https://rapidoc.croapp.cz/index.html ->
    url = "https://rapidoc.croapp.cz/apifile/openapi.yaml"
    ydata = _helpers.request_url_yaml(url)
    _helpers.pp(ydata)


def test_dict_list_to_rows():
    url = "https://rapidev.croapp.cz/stations?"
    jdata = _helpers.request_url_json(url)
    assert jdata is not None
    sdata = jdata["data"]
    rows, header = _helpers.dict_list_to_rows(sdata)
    _helpers.save_rows_to_csv("./runtime2/stations.csv", rows, header)
    tdata = _helpers.rows_transpose([header])
    _helpers.save_rows_to_csv("./runtime2/stations_fields.csv", tdata)


def test_json_to_csv() -> None:
    url = "https://rapidev.croapp.cz/stations?"
    jdata = _helpers.request_url_json(url)
    assert jdata is not None
    paths = _helpers.dict_paths_vectors(jdata, list())
    print(paths)
    # print(jdata['data'])
    paths = _helpers.dict_paths_vectors(jdata["data"][0], list())
    print(paths)
    # _helpers.dict_to_csv(jdata)
    # _helpers.dict_to_csv(jdata['meta'])
