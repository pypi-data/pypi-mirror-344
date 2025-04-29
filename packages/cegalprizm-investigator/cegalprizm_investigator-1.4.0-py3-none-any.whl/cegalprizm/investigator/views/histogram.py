# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the HistogramView class
"""

from typing import List, Sequence, Union

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..inv.investigation import Investigation
from .investigator_window_predefined_view import InvestigatorWindowPredefinedView
from .options_histograms import OptionsHistogram
from .predefined_view_tuple import PredefinedViewTuple

class HistogramView(InvestigatorWindowPredefinedView, OptionsHistogram):
    """A class representing a HistogramView

    The view defines how a histogram should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "Histogram")

    def copy(self):
        """Create a copy of this view

        Returns:
            HistogramView: the copied view
        """
        copy = HistogramView(None)
        copy._investigation = self._investigation
        copy._plot_type = self._plot_type
        copy._options = self._options
        copy._data.CopyFrom(self._data)
        copy._dataset_priority_order = list(self._dataset_priority_order)
        return copy

    ######################################################################
    # Multi-Views
    ######################################################################

    def create_dimension_views(self, dimensions: Union[str, Sequence[str]] = "all") -> List[PredefinedViewTuple]:
        """Creates a copy of this view for each dimension specified

        Args:
            dimensions (Union[str, Sequence[str]], optional): Defaults to 'all'.
                                - 'all' will duplicate the view for all the continuous dimensions in the investigation
                                - a list of continuous dimensions to be used

        Returns:
            List[PredefinedViewTuple]: a list of views; one per specified dimension
        """
        if dimensions is None:
            raise ValueError("dimensions must be defined")
        elif dimensions == "all":
            dimensions = [x.name for x in self._investigation._continuous_dimensions()]
        elif isinstance(dimensions, list):
            if len(dimensions) == 0:
                raise ValueError("dimensions must contain at least 1 entry")
        else:
            raise ValueError("dimensions is not valid")

        views = []
        for name in dimensions:
            view = self.copy()
            view.set_dimension(name)
            views.append(PredefinedViewTuple(name=name, view=view))
        return views

    ######################################################################
    # General settings
    ######################################################################

    def swap_axes(self):
        """Toggle whether the axes should be swapped in the view
        """
        self._data.general_settings.swap_axes = not self._data.general_settings.swap_axes

    ######################################################################
    # Display by data settings
    ######################################################################

    def set_dimension(self, dimension: str):
        """Sets the dimension to be shown in the histogram

        Args:
            dimension (str): The name of the dimension to be used

        Raises:
            ValueError: if the dimension is not a valid continuous dimension
        """
        dimension_id = super(HistogramView, self)._get_continuous_id(dimension)
        self._data.display_by_data.selected_dimension_x = dimension_id

    def show_multi_histograms(self, show: bool):
        """Set whether the histogram should be shown as a multi-dimension histogram

        Args:
            show (bool): Should the multi-dimension histogram be shown
        """
        self._data.histogram_settings.show_multi_histograms = show
        if len(self._data.display_by_data.selected_dimensions) == 0:
            ids = [super(HistogramView, self)._get_continuous_id(name) for name in self._investigation.continuous_dimension_names]
            self._data.display_by_data.selected_dimensions.extend(ids)

    def set_dimensions(self, dimension_names: Sequence[str]):
        """Sets the dimensions to be shown in the multi histogram

        Args:
            dimension_names (Sequence[str]): A list of the names of the dimensions to be used

        Raises:
            ValueError: if the dimension is not a valid continuous dimension
        """
        if dimension_names is None:
            raise ValueError("dimension_names must be defined")
        if not isinstance(dimension_names, list):
            raise ValueError("dimension_names must be a list of strings")
        if len(dimension_names) == 0:
            raise ValueError("dimension_names must contain at least 1 entry")
        for name in dimension_names:
            if name not in self._investigation.continuous_dimension_names:
                raise ValueError(f"dimension_names list should only contain {str(self._investigation.continuous_dimension_names)}")

        ids = [super(HistogramView, self)._get_continuous_id(name) for name in dimension_names]
        del self._data.display_by_data.selected_dimensions[:]
        self._data.histogram_settings.show_multi_histograms = True
        self._data.display_by_data.selected_dimensions.extend(ids)

    def set_barchart(self, barchart_option: str):
        """Set the bar chart option to be displayed

        Args:
            barchart_option (str): The name of the discrete dimension to be used

        Raises:
            ValueError: if the discrete dimension is not valid in the investigation
        """
        option = next((x.id for x in self._options.histogram_settings.available_barchart_options if x.name == barchart_option), None)
        if option is None:
            options = [x.name for x in self._options.histogram_settings.available_barchart_options]
            raise ValueError(f"barchart_option ('{barchart_option}') must be one of {str(options)}")
        self._data.histogram_settings.selected_barchart_option = option
        self._data.histogram_settings.show_as_piechart = False

    def set_barchart_statistic(self, barchart_statistic: str):
        """Set the bar chart statistic to be displayed

        Args:
            barchart_statistic (str): The name of the statistic to be used in the bar chart

        Raises:
            ValueError: if the barchart statistic is not valid
        """
        if barchart_statistic not in self._options.histogram_settings.available_barchart_statistics:
            raise ValueError(f"barchart_statistic ('{barchart_statistic}') must be one of {str(self._options.histogram_settings.available_barchart_statistics)}")
        self._data.histogram_settings.selected_barchart_statistic = barchart_statistic

    def set_piechart(self, piechart_option: str):
        """Set the pie chart option to be displayed

        Args:
            piechart_option (str): The name of the discrete dimension to be used

        Raises:
            ValueError: if the discrete dimension is not valid in the investigation
        """
        option = next((x.id for x in self._options.histogram_settings.available_barchart_options if x.name == piechart_option), None)
        if option is None:
            options = [x.name for x in self._options.histogram_settings.available_barchart_options]
            raise ValueError(f"piechart_option ('{piechart_option}') must be one of {str(options)}")
        self._data.histogram_settings.selected_barchart_option = option
        self._data.histogram_settings.show_as_piechart = True

    def set_piechart_statistic(self, piechart_statistic: str):
        """Set the pie chart statistic to be displayed

        Args:
            piechart_statistic (str): The name of the statistic to be used in the pie chart

        Raises:
            ValueError: if the barchart statistic is not valid
        """
        if piechart_statistic not in self._options.histogram_settings.available_barchart_statistics:
            raise ValueError(f"piechart_statistic ('{piechart_statistic}') must be one of {str(self._options.histogram_settings.available_barchart_statistics)}")
        self._data.histogram_settings.selected_barchart_statistic = piechart_statistic

    def apply_weighting(self, apply_weighting: bool, weighting_option: str = None):
        """Set whether to apply weighting to the histogram values

        Args:
            apply_weighting (bool): If True then weighting will be applied to the histogram
            weighting_option (str): If True then weighting will be applied to the histogram
        """

        option = next((x.id for x in self._options.histogram_settings.available_weighting_options if x.name == weighting_option), None)
        if option is None:
            options = [x.name for x in self._options.histogram_settings.available_weighting_options]
            raise ValueError(f"weighting_option ('{weighting_option}') must be one of {str(options)}")

        self._data.histogram_settings.apply_weighting = apply_weighting
        self._data.histogram_settings.selected_weighting_option = option

    ######################################################################
    # Statistics
    ######################################################################

    def set_draw_statistics(self, draw_statistics: bool):
        """Set whether the statistics should be shown

        Args:
            show (bool): Should the statistics be shown
        """
        self._data.statistics_settings.draw_statistics = draw_statistics
