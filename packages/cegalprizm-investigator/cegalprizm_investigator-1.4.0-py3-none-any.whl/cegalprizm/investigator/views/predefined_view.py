# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the PredefinedView class

This class is internal and is only exposed via inheritance
"""

from typing import List, Tuple

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from google.protobuf.json_format import MessageToJson
from google.protobuf.any_pb2 import Any

from ..exceptions import CegalHubError, InvestigatorViewError
from ..inv.investigation import Investigation
from ..protos import investigator_api_pb2
from ..protos import predefined_view_pb2

class PredefinedView:
    """The base class from which all other views inherit
    """

    def __init__(self, investigation: Investigation, plot_type: str):

        if investigation is not None:
            supported_plot_tuple = self._is_plot_supported(investigation, plot_type)
            if not supported_plot_tuple[0]:
                raise InvestigatorViewError(supported_plot_tuple[1])

        self._investigation = investigation
        self._plot_type = plot_type
        self._options = predefined_view_pb2.AvailableOptions()
        self._data = predefined_view_pb2.PredefinedViewData()
        self._dataset_priority_order: List[str] = list()

        if investigation is not None:
            msg = investigator_api_pb2.GetPredefinedViewRequest()
            msg.investigation_id.id = self._investigation.id
            msg.plot = investigator_api_pb2.PlotEnum.Value(self._plot_type)
            payload = Any()
            payload.Pack(msg)

            result = self._investigation._hub_context.do_unary_request("investigator.GetPredefinedView", payload)
            if result[0]:
                response = investigator_api_pb2.GetPredefinedViewResponse()
                result[1].Unpack(response)
                self._options = response.available_options
                self._data.CopyFrom(response.view)
            else:
                raise CegalHubError(result[1])

    def get_json(self) -> str:
        """Gets the json string representing the current view

        Returns:
            str: The json string
        """
        return MessageToJson(self._data, including_default_value_fields=True)

    def _set_testing(self, is_testing: bool) -> None:
        self._data.test_image = is_testing

    ######################################################################
    # Private methods
    ######################################################################

    def _is_plot_supported(self, investigation: Investigation, plot_type: str) -> Tuple[bool, str]:
        error_message = next((x.error_message for x in investigation._summary.supported_plots if x.plot == investigator_api_pb2.PlotEnum.Value(plot_type)), None)
        return (len(error_message) == 0, error_message)

    def _get_continuous_id(self, dimension_name: str) -> str:
        dimension_id = next((x.id for x in self._investigation._continuous_dimensions() if x.name == dimension_name), None)
        if dimension_id is None:
            options = [x.name for x in self._investigation._continuous_dimensions()]
            raise ValueError(f"dimension_name ('{dimension_name}') must be one of {str(options)}")
        return dimension_id

    def _get_discrete_id(self, name: str)-> str:
        discrete_tuples = self._investigation._discrete_tuples()
        for key in discrete_tuples.keys():
            tuples = discrete_tuples[key]
            for named_tuple in tuples:
                if named_tuple.name == name:
                    return named_tuple.id
        return None

    def _get_color_by_id(self, color_by_option: str) -> str:
        option_id = next((x.id for x in self._options.display_by_data.available_color_bys if x.name == color_by_option), None)
        if option_id is None:
            options = [x.name for x in self._options.display_by_data.available_color_bys]
            raise ValueError(f"color_by_option ('{color_by_option}') must be one of {str(options)}")
        return option_id

    def _get_appearance_by_id(self, appearance_by_option: str) -> str:
        option_id = next((x.id for x in self._options.display_by_data.available_appearance_bys if x.name == appearance_by_option), None)
        if option_id is None:
            options = [x.name for x in self._options.display_by_data.available_appearance_bys]
            raise ValueError(f"appearance_by_option ('{appearance_by_option}') must be one of {str(options)}")
        return option_id
