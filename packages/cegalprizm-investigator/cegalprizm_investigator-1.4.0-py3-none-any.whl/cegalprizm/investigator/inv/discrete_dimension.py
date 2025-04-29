﻿# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the DiscreteDimension class
"""

from typing import Union

import ctypes

# pylint: disable=relative-beyond-top-level

from ..protos import investigation_pb2
from ..utils import _get_shape, _clamp_size, _color_name_to_int


class DiscreteDimension:
    """A class representing a discrete dimension in a Blueback Investigation

    This object provides the API to be used to set/get information about a specific discrete dimension
    """

    def __init__(self, investigation, dimension_info: investigation_pb2.DiscreteDimensionInfo):
        self._investigation = investigation
        self._dimension_info = dimension_info

    def set_name(self, name: str):
        """Set the name to be used for this dimension

        Args:
            name (str): The name to be used

        Raises:
            ValueError: if name is undefined or empty
        """
        if name is None:
            raise ValueError("name must be defined")
        if len(name) == 0:
            raise ValueError("name cannot be empty")

        self._dimension_info.name = name

    def set_color(self, color: Union[int, str]):
        """Set the color to be used for this dimension

        Args:
            color (Union[int, str]): Either the int value or the webcolor colorname to be used for the dataset color

        Raises:
            ValueError: if color is not an int or a recognised webcolor colorname
        """
        if isinstance(color, int):
            col = color
        elif isinstance(color, str):
            col = _color_name_to_int(color)
        else:
            raise ValueError("color must be int or str")

        self._dimension_info.group.color = ctypes.c_int32(col).value

    def set_entry_name(self, name: str, new_name: str):
        """Set the name to be used for the entry

        Args:
            name (str): The name of the entry to be updated
            new_name (str): The new entry name

        Raises:
            ValueError: if no entry can be found by the given name
            ValueError: if new_name is undefined or empty
        """
        if name is None:
            raise ValueError("name must be defined")
        if len(name) == 0:
            raise ValueError("name cannot be empty")
        if new_name is None:
            raise ValueError("name must be defined")
        if len(new_name) == 0:
            raise ValueError("name cannot be empty")

        entry = self._get_entry_by_name(name)
        entry.option_name = new_name

    def set_entry_color(self, name: str, color: Union[int, str]):
        """Set the color to be used for the entry

        Args:
            name (str): The name of the entry to be updated
            color (Union[int, str]): Either the int value or the webcolor colorname to be used for the dataset color

        Raises:
            ValueError: if no entry can be found by the given name
            ValueError: if color is not an int or a recognised webcolor colorname
        """
        if name is None:
            raise ValueError("name must be defined")
        if len(name) == 0:
            raise ValueError("name cannot be empty")

        if isinstance(color, int):
            col = color
        elif isinstance(color, str):
            col = _color_name_to_int(color)
        else:
            raise ValueError("color must be int or str")

        entry = self._get_entry_by_name(name)
        entry.value.color = ctypes.c_int32(col).value

    def set_entry_shape(self, name: str, shape: str, size: int):
        """Set the shape to be used for the entry

        Args:
            shape (str): The name of the shape to be used
            size (int): The size of the shape to be used

        Raises:
            ValueError: The name of the entry to be updated
            ValueError: If the shape string is not a valid option
            ValueError: If the size is not a valid option
        """
        if name is None:
            raise ValueError("name must be defined")
        if len(name) == 0:
            raise ValueError("name cannot be empty")
        if size < 1:
            raise ValueError("size must be greater than 0")
            
        entry = self._get_entry_by_name(name)
        entry.value.style.shape = _get_shape(shape)
        entry.value.style.shape_size = _clamp_size(size)

    def _get_entry_by_name(self, name: str):
        # print(list(self._get_entries()))
        entry = next((x for x in self._get_entries() if x[0] == name), None)
        if entry is None:
            options = [x[0] for x in self._get_entries()]
            raise ValueError(f"name ('{name}') must be one of {str(options)}")
        return entry[1]

    def _get_entries(self):
        for entry in _get_discrete_entries(self._dimension_info.group.options):
            if entry is not None:
                yield entry


def _get_discrete_entries(options, prefix: str = ''):
    for option in options:
        yield (prefix + option.option_name, option)
        if len(option.group.options) > 0:
            for entry in _get_discrete_entries(option.group.options, prefix + option.group.name + '/'):
                yield entry
