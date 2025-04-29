# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the method to refresh the local cached investigation object from the server
"""

from typing import Iterable, Tuple, Type

from google.protobuf.any_pb2 import Any
import pandas as pd

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..exceptions import CegalHubError
from ..protos import investigation_pb2
from ..protos import investigator_api_pb2

from .investigation import Investigation

def _refresh(investigation: Type[Investigation]):
    msg = investigator_api_pb2.InvestigationId(id=investigation.id)
    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.GetContinuousDimensions", payload)
    if result[0]:
        response1 = investigator_api_pb2.ContinuousDimensionInfoCollection()
        result[1].Unpack(response1)
        investigation._data._continuous_dimensions = response1
        response2 = investigator_api_pb2.ContinuousDimensionInfoCollection()
        result[1].Unpack(response2)
        investigation._original._continuous_dimensions = response2
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetDiscreteDimensions", payload)
    if result[0]:
        response1 = investigator_api_pb2.DiscreteDimensionInfoCollection()
        result[1].Unpack(response1)
        investigation._data._discrete_dimensions = response1
        response2 = investigator_api_pb2.DiscreteDimensionInfoCollection()
        result[1].Unpack(response2)
        investigation._original._discrete_dimensions = response2
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetClassifications", payload)
    if result[0]:
        response1 = investigation_pb2.Classifications()
        result[1].Unpack(response1)
        investigation._data._classification_groups = response1
        response2 = investigation_pb2.Classifications()
        result[1].Unpack(response2)
        investigation._original._classification_groups = response2
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetRestrictions", payload)
    if result[0]:
        response1 = investigation_pb2.Restrictions()
        result[1].Unpack(response1)
        investigation._data._restrictions = response1
        response2 = investigation_pb2.Restrictions()
        result[1].Unpack(response2)
        investigation._original._restrictions = response2
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetDatasets", payload)
    if result[0]:
        response1 = investigator_api_pb2.DatasetInfoCollection()
        result[1].Unpack(response1)
        investigation._data._datasets = response1
        response2 = investigator_api_pb2.DatasetInfoCollection()
        result[1].Unpack(response2)
        investigation._original._datasets = response2
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetInvestigationInfo", payload)
    if result[0]:
        response1 = investigator_api_pb2.InvestigationInfo()
        result[1].Unpack(response1)
        investigation._data._info = response1
        response2 = investigator_api_pb2.InvestigationInfo()
        result[1].Unpack(response2)
        investigation._original._info = response2
    else:
        raise CegalHubError(result[1])

    def _get_additional_discrete(investigation, datasets) -> Iterable[Tuple[str, Type]]:
        for dataset_tuple in investigation._get_datasets(datasets):
            for visibility in dataset_tuple[0].data_visibilities:
                yield (dataset_tuple[0].id, visibility)

    investigation._data._dataset_additional_discrete = list(_get_additional_discrete(investigation, investigation._data._datasets))
    investigation._original._dataset_additional_discrete = list(_get_additional_discrete(investigation, investigation._original._datasets))

    try:
        investigation._epoch_timestamp = pd.Timestamp.fromtimestamp(investigation._data._info.min_date.seconds)
    except:
        investigation._epoch_timestamp = None
