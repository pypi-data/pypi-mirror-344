# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the TimeSeriesView class
"""

from typing import List, Sequence, Union

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..constants import DATE_SPATIAL_DIMENSION_NAME
from ..inv.investigation import Investigation
from .investigator_window_predefined_view import InvestigatorWindowPredefinedView
from .predefined_view_tuple import PredefinedViewTuple

class TimeSeriesView(InvestigatorWindowPredefinedView):
    """A class representing a TimeSeriesView

    The view defines how a time series plot should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "TimeSeries")

    def copy(self):
        """Create a copy of this view

        Returns:
            TimeSeriesView: the copied view
        """
        copy = TimeSeriesView(None)
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
            view.set_left_dimensions([name])
            views.append(PredefinedViewTuple(name=name, view=view))
        return views

    ######################################################################
    # General settings
    ######################################################################

    def tile_plots(self, tile: bool):
        """Set whether plots should be tiled or not

        Args:
            show (bool): Should the plots be tiled
        """
        self._data.time_series_settings.tile_plots = tile

    def show_plot_titles(self, show: bool):
        """Set whether plot titles should be shown

        Args:
            show (bool): Should the plot titles be shown
        """
        self._data.time_series_settings.show_plot_titles = show

    ######################################################################
    # Display by data settings
    ######################################################################

    def set_left_dimensions(self, dimension_names: Sequence[str]):
        """Sets the left dimensions to be shown in the time series plot

        Args:
            dimension_names (Sequence[str]): A list of the names of the dimensions to be used

        Raises:
            ValueError: if the dimension is not a valid continuous dimension
        """
        if dimension_names is not None:
            if not isinstance(dimension_names, list):
                raise ValueError("dimension_names must be a list of strings or None")
            if len(dimension_names) == 0:
                raise ValueError("dimension_names must contain at least 1 entry")
            for name in dimension_names:
                if name not in self._investigation.continuous_dimension_names:
                    raise ValueError(f"dimension_names list should only contain {str(self._investigation.continuous_dimension_names)}")

        if dimension_names is None:
            ids = []
        else:
            ids = [super(TimeSeriesView, self)._get_continuous_id(name) for name in dimension_names if name != DATE_SPATIAL_DIMENSION_NAME]
        del self._data.display_by_data.selected_left_dimensions[:]
        self._data.display_by_data.selected_left_dimensions.extend(ids)

    def set_right_dimensions(self, dimension_names: Sequence[str]):
        """Sets the right dimensions to be shown in the time series plot

        Args:
            dimension_names (Sequence[str]): A list of the names of the dimensions to be used

        Raises:
            ValueError: if the dimension is not a valid continuous dimension
        """
        if dimension_names is not None:
            if not isinstance(dimension_names, list):
                raise ValueError("dimension_names must be a list of strings")
            if len(dimension_names) == 0:
                raise ValueError("dimension_names must contain at least 1 entry")
            for name in dimension_names:
                if name not in self._investigation.continuous_dimension_names:
                    raise ValueError(f"dimension_names list should only contain {str(self._investigation.continuous_dimension_names)}")

        if dimension_names is None:
            ids = []
        else:
            ids = [super(TimeSeriesView, self)._get_continuous_id(name) for name in dimension_names if name != DATE_SPATIAL_DIMENSION_NAME]
        del self._data.display_by_data.selected_right_dimensions[:]
        self._data.display_by_data.selected_right_dimensions.extend(ids)

    def show_multi_plot(self, show: bool):
        """Set whether the time series window should be shown as a multi-plot window

        Args:
            show (bool): Should the window be shown as multi-plot
        """
        self._data.time_series_settings.show_multi_plot = show

    ######################################################################
    # General settings
    ######################################################################

    def show_fans(self, show: bool):
        """Set whether fans should be shown

        Args:
            show (bool): Should the fans be shown
        """
        if show:
            self._data.time_series_settings.show_fans = "show"
        else:
            self._data.time_series_settings.show_fans = "hide"

    def show_individual_children(self, show: bool):
        """Set whether individual children should be shown

        Args:
            show (bool): Should the individual children be shown
        """
        if show:
            self._data.time_series_settings.show_individual_children = "show"
        else:
            self._data.time_series_settings.show_individual_children = "hide"
