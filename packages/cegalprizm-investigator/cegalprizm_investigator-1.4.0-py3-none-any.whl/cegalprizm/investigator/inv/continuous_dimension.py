# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the ContinuousDimension class
"""

# pylint: disable=relative-beyond-top-level

from typing import Union

import pandas as pd
import ctypes
from datetime import datetime

from ..protos import investigation_pb2
from ..utils import _get_numeric_precision, _clamp_precision_value, _color_name_to_int

class ContinuousDimension:
    """A class representing a continuous dimension in a Blueback Investigation

    This object provides the API to be used to set/get information about a specific continuous dimension
    """

    def __init__(self, investigation, dimension_info: investigation_pb2.ContinuousDimensionInfo):
        self._investigation = investigation
        self._dimension_info = dimension_info

    def set_name(self, name: str):
        """Set the name to be used for this dimension

        Note: Changes are applied by calling :py:func:Investigation.refresh()

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
            color (Union[int, str]): Either the int value or the webcolor colorname to be used for the dimension color

        Raises:
            ValueError: if color is not an int or a recognised webcolor colorname
        """
        if isinstance(color, int):
            col = color
        elif isinstance(color, str):
            col = _color_name_to_int(color)
        else:
            raise ValueError("color must be int or str")

        self._dimension_info.color = ctypes.c_int32(col).value

    def set_display_units(self, symbol: str):
        """Set the display unit to be used for this dimension

        Args:
            symbol (str): The display unit to be used

        Raises:
            ValueError: The provided symbol is not valid for this dimension
        """
        if symbol not in self._dimension_info.available_units:
            raise ValueError(f"symbol ('{symbol}') must be one of {str(self._dimension_info.available_units)}")

        self._dimension_info.display_units = symbol

    def set_precision(self, precision: str, value: int):
        """Set the precision format to be used for this dimension

        Args:
            precision (str): The type of precision to be applied ['decimalplaces', 'significantfigures', 'engineering']
            value (int): The precision value to to applied. eg number of decimal places

        Raises:
            ValueError: If the precision string is not a valid option
            ValueError: If the value is not a valid option for the provided precision
        """
        self._dimension_info.precision.precision = _get_numeric_precision(precision)
        self._dimension_info.precision.value = _clamp_precision_value(self._dimension_info.precision.precision, value)

    def set_axis_logarithmic(self, is_logarithmic: bool):
        """Set the dimension to be displayed as logarithmic

        Args:
            is_logarithmic (bool): Whether to display as logarithmic or not
        """
        self._dimension_info.view.is_logarithmic = is_logarithmic

    def set_axis_reversed(self, is_reversed: bool):
        """Set the dimension to be displayed as reversed

        Args:
            is_reversed (bool): Whether to reverse the axis or not
        """
        self._dimension_info.view.is_reversed = is_reversed

    def set_axis_symmetric(self, is_symmetric: bool):
        """Set the dimension to be displayed as symmetrical

        Args:
            is_symmetric (bool): Whether to display as symmetrical or not
        """
        self._dimension_info.view.is_symmetric = is_symmetric

    def set_range(self, min_value: Union[float, str], max_value: Union[float, str]):
        """Set the range to be used for the dimension

        If either value is set to None then the appropriate value will be determined from the investigation data

        Args:
            min_value (Union[float, str]): The minimum value to tbe used for the dimension range
            max_value (Union[float, str]): The maximum value to tbe used for the dimension range
        """
        if self._dimension_info.type == investigation_pb2.DimensionEnum.Date:
            if min_value is not None:
               try:
                    date = pd.Timestamp(datetime.fromisoformat(min_value))
                    min_value = self._investigation._get_offset_from_date(date)
               except Exception:
                   raise ValueError("min_value must be a valid isoformat datetime")
            if max_value is not None:
                try:
                    date = pd.Timestamp(datetime.fromisoformat(max_value))
                    max_value = self._investigation._get_offset_from_date(date)
                except Exception:
                    raise ValueError("max_value must be a valid isoformat datetime")
        else:
            if min_value is not None and not (isinstance(min_value, float) or isinstance(min_value, int)):
                raise ValueError("min_value must be a float")
            if max_value is not None and not (isinstance(max_value, float) or isinstance(max_value, int)):
                raise ValueError("max_value must be a float")

        if min_value is None:
            self._dimension_info.view.range.is_min_manual = False
        else:
            self._dimension_info.view.range.is_min_manual = True
            self._dimension_info.view.range.manual_extents.min = min_value

        if max_value is None:
            self._dimension_info.view.range.is_max_manual = False
        else:
            self._dimension_info.view.range.is_max_manual = True
            self._dimension_info.view.range.manual_extents.max = max_value

    def set_number_of_bins(self, value: int):
        """Set the number of histogram bins into which the dimension range should be split

        Args:
            value (int): The number of bins to be used

        Raises:
            ValueError: If the value is not greater than 0
        """
        if value <= 0:
            raise ValueError("value must be > 0")

        self._dimension_info.view.bins.use_bin_size = False
        self._dimension_info.view.bins.num_bins = value

    def set_bin_size(self, value: float):
        """Set the bin size which should be applied to the dimension range

        Args:
            value (float): The size of the bin to be used

        Raises:
            ValueError: If the value is 0
        """
        if value == 0:
            raise ValueError("value must not be equal to 0")

        self._dimension_info.view.bins.use_bin_size = True
        self._dimension_info.view.bins.bin_size = value
