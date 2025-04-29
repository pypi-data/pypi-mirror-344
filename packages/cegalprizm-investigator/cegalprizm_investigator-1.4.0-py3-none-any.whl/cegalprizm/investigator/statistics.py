# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the methods to be used to the statistics associated with a particular view
"""

from google.protobuf.any_pb2 import Any
import pandas as pd

# pylint: disable=relative-beyond-top-level

from .exceptions import CegalHubError
from .protos import investigator_api_pb2
from .views.predefined_view import PredefinedView


def get_statistics(view: PredefinedView, dimension: str = None) -> pd.DataFrame:
    """Gets the dimension statistics data based on the provided view

    Args:
        view (PredefinedView): The view defining how investigation should be reported
        dimension (str): The name of the continuous dimension for which the statistics should be obtained

    Raises:
        ValueError: if view is not defined
        CegalHubError: if an unexpected error is reported by Hub

    Returns:
        pandas.DataFrame: A dataframe containing the statistics
    """
    if view is None:
        raise ValueError("view must be defined")

    if dimension is None:
        dimension_id = view._investigation._continuous_dimensions()[0].id
    else:
        dimension_id = view._get_continuous_id(dimension)

    msg = investigator_api_pb2.GetStatisticsRequest(view=view._data)
    msg.investigation_id.id = view._investigation.id
    msg.plot = investigator_api_pb2.PlotEnum.Value(view._plot_type)
    msg.dimension_id = dimension_id

    payload = Any()
    payload.Pack(msg)

    result = view._investigation._hub_context.do_unary_request("investigator.GetStatistics", payload)
    if result[0]:
        response = investigator_api_pb2.GetStatisticsResponse()
        result[1].Unpack(response)
        return pd.DataFrame.from_records([(s.name, s.count, s.min, s.max, s.delta, s.mean, s.median, s.stddev, s.variance) for s in response.collection],
                                          columns=["Name", "Count", "Min", "Max", "Delta", "Mean", "Median", "Stddev", "Variance"])
    else:
        raise CegalHubError(result[1])
