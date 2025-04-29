from copy import deepcopy
from lens import etch
from pytest import fixture, raises


@fixture
def collection_deep():
    return {"a": {"b": {"c": {"d": {"e": {"f": "z"}}}}}}


@fixture
def collection_simple():
    return {"a": "aye", "b": "bee", "c": ["see", "sea"]}


@fixture
def value():
    return "value"


def test_etch_simple(collection_simple, value):
    keys = ["d"]
    observed = etch.carve(deepcopy(collection_simple), keys, value)
    collection = deepcopy(collection_simple)
    collection["d"] = value
    expected = collection
    assert observed == expected


def test_etch_less_keys_than_depth(collection_deep, value):
    keys = ["a", "b", "c"]
    observed = etch.carve(collection_deep, keys, value)
    expected = {"a": {"b": {"c": value}}}
    assert observed == expected


def test_etch_overwrite_into_array(collection_simple, value):
    expected = {"a": "aye", "b": "bee", "c": [value, "sea"]}
    keys = ["c", 0]
    observed = etch.carve(collection_simple, keys, value)
    assert observed == expected


def test_etch_append_to_list(collection_simple, value):
    expected = {"a": "aye", "b": "bee", "c": ["see", "sea", value]}
    keys = ["c", 2]
    observed = etch.carve(collection_simple, keys, value)
    assert observed == expected


def test_etch_non_integer_to_list(collection_simple, value):
    keys = ["c", "zz"]
    with raises(etch.EtchingError):
        etch.carve(collection_simple, keys, value)


def test_etch_too_high_index_to_list(collection_simple, value):
    keys = ["c", 99]
    with raises(etch.EtchingError):
        etch.carve(collection_simple, keys, value)


def test_etch_deep_to_dict(collection_simple, value):
    keys = ["a", "b", "c", "d", "d"]
    observed = etch.carve(deepcopy(collection_simple), keys, value)
    expected = {"a": {"b": {"c": {"d": {"d": value}}}}, "b": "bee", "c": ["see", "sea"]}
    assert observed == expected
