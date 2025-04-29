# Copyright 2025 Nathan Menge - nathan.menge@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This module is included as it is useful to this project and I wasn't ready to open source it, but hopefully I will do
# that soon.  At which point I will remove this and pull it as a dependency through pip.

from lens import FocusingError
from typing import Any, Hashable


class EtchingError(ValueError):
    pass


class StepBackUp(ValueError):
    pass


def etch(
    collection: dict | list,
    keys: list[Hashable],
    value: Any,
):
    try:
        collection_leaf, remaining_keys, terminal_key = descend_collection(collection, keys)
    except FocusingError as fe:
        raise EtchingError(f"Could not etch value '{value}' into collection {collection}, at key chain {keys}") from fe

    new_structure = construct_data_structure(remaining_keys, value)
    combine(collection_leaf, terminal_key, new_structure)
    return collection


def combine(collection, terminal_key, new_structure):
    try:
        collection[terminal_key] = new_structure
    except IndexError:
        if len(collection) != terminal_key:
            raise EtchingError(f"Cannot etch to specified index, {terminal_key} in list {collection}")
        collection.append(new_structure)
    return collection


def construct_data_structure(keys: list[Hashable], value: Any) -> dict[Hashable, Any]:
    """
    This function creates a dict from the keys, at the bottom of which, the value is placed
    This function works recursively.
    :param keys: Keys for the nested dict
    :param value: Value to place at the end lead of the structure
    :return: Returns the created structure
    """
    if not keys:
        return value  # type: ignore
    return {(keys.pop(0)): construct_data_structure(keys, value)}


def descend_collection(collection: dict | list, keys: list[Hashable]) -> tuple[dict | list, list[Hashable], Hashable]:
    current_key: Hashable = keys.pop(0)
    try:
        current_collection = collection[current_key]  # type: ignore
    except (KeyError, IndexError):
        return collection, keys, current_key
    except TypeError:
        if isinstance(collection, str):
            keys.insert(0, current_key)
            raise StepBackUp() from None
        raise FocusingError(f"Cannot descend collection via key {current_key} in collection {collection}")
    if not keys:
        return collection, keys, current_key
    try:
        return descend_collection(current_collection, keys)
    except StepBackUp:
        return collection, keys, current_key
