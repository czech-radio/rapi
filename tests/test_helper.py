from rapi import helpers

nested_dict = {
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
}


def test_dict_get() -> None:
    val = helpers.dict_get(nested_dict, ["person1", "name"])
    assert val == "John Doe"
    val = helpers.dict_get(nested_dict, ["person1", "contact", "email"])
    assert val == "john@example.com"


def test_deep_merge_dicts():
    dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
    dict2 = {"b": {"y": "ahoj", "z": 40}, "c": 3}
    merged_dict = helpers.deep_merge_dicts(dict1, dict2)
    print(merged_dict)
