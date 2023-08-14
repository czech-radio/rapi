from typing import Union

from rapi import helpers

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
    res = helpers.dict_paths_vectors(nested_dict, list())
    print(res)


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


def test_request_url_json() -> None:
    print()
    url = "https://rapidev.croapp.cz/stations?"
    # url="https://rapidev.croapp.cz/stations?page[1]=0&page[limit]=1"
    jdata = helpers.request_url_json(url)
    assert jdata


def test_request_url_yaml() -> None:
    ### urls:
    # https://rapidoc.croapp.cz/index.html ->
    url = "https://rapidoc.croapp.cz/apifile/openapi.yaml"
    ydata = helpers.request_url_yaml(url)
    helpers.pp(ydata)


def test_dict_list_to_rows():
    url = "https://rapidev.croapp.cz/stations?"
    jdata = helpers.request_url_json(url)
    assert jdata is not None
    sdata = jdata["data"]
    rows, header = helpers.dict_list_to_rows(sdata)
    helpers.save_rows_to_csv("./runtime2/stations.csv", rows, header)
    tdata = helpers.rows_transpose([header])
    helpers.save_rows_to_csv("./runtime2/stations_fields.csv", tdata)


def test_json_to_csv() -> None:
    url = "https://rapidev.croapp.cz/stations?"
    jdata = helpers.request_url_json(url)
    assert jdata is not None
    paths = helpers.dict_paths_vectors(jdata, list())
    print(paths)
    # print(jdata['data'])
    paths = helpers.dict_paths_vectors(jdata["data"][0], list())
    print(paths)
    # helpers.dict_to_csv(jdata)
    # helpers.dict_to_csv(jdata['meta'])
