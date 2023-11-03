import pytest

import rapi._shared as _shared

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


@pytest.mark.shared
def test_dict_get_path() -> None:
    val = _shared.dict_get_path(nested_dict, ["person1", "name"])
    assert val == "John Doe"
    val = _shared.dict_get_path(nested_dict, ["person1", "contact", "email"])
    assert val == "john@example.com"


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


@pytest.mark.shared
def test_parse_date_optional_fields() -> None:
    sd = sample_dates
    _func = _shared.parse_date_optional_fields
    result1 = _func(sd[-1])
    result2 = _func(sd[-2])
    assert result1 < result2
