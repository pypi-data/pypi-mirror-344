# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains a private method which should only be used internally
"""

from typing import Dict, Sequence

import numpy as np
import pandas as pd
from google.protobuf.any_pb2 import Any
from google.protobuf.timestamp_pb2 import Timestamp

# pylint: disable=relative-beyond-top-level
# pylint: disable=logging-fstring-interpolation

from . import logger
from .constants import *
from .named_tuples import ContinuousDimensionInfoTuple
from .exceptions import CegalHubError
from .hub_context import InvPyHubContext
from .inv.investigation import Investigation
from .protos import investigation_pb2
from .protos import investigator_api_pb2
from .utils import _pack_payloads, _get_offset_from_date

_WELL_KNOWN_SPATIAL_COLUMN_NAMES = {
    X_SPATIAL_DIMENSION_NAME: investigation_pb2.DimensionEnum.X,
    Y_SPATIAL_DIMENSION_NAME: investigation_pb2.DimensionEnum.Y,
    Z_SPATIAL_DIMENSION_NAME: investigation_pb2.DimensionEnum.Z,
    TVD_SPATIAL_DIMENSION_NAME: investigation_pb2.DimensionEnum.Z,
    TWT_SPATIAL_DIMENSION_NAME: investigation_pb2.DimensionEnum.Twt,
    DATE_SPATIAL_DIMENSION_NAME: investigation_pb2.DimensionEnum.Date
    }

_WELL_KNOWN_SAMPLE_INDEX_COLUMN_NAMES = ["I", "J", "K"]

_NUM_ROWS_PER_CHUNK = 10000

def _from_dataframe(context: InvPyHubContext,
                    dataframe: pd.DataFrame,
                    continuous_column_names: Sequence[str] = None,
                    continuous_column_info: Dict[str, ContinuousDimensionInfoTuple] = None,
                    discrete_column_names: Sequence[str] = None,
                    dataset_column_name: str = None,
                    sample_index_column_names: Sequence[str] = None):

    if dataframe is None:
        raise ValueError("dataframe must specified")

    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("dataframe must be of type pd.DataFrame")

    if dataframe.shape[0] == 0:
        raise ValueError("dataframe must contain at least 1 row")

    if dataframe.shape[1] == 0:
        raise ValueError("dataframe must contain at least 1 continuous column")

    if len(dataframe.columns) != len(set(dataframe.columns)):
        raise ValueError("dataframe column names must be unique")

    guess_continuous_names = []
    guess_discrete_names = []
    guess_spatial_names = []
    guess_sample_index_names = []
    guess_dataset_column_name = None

    for col in dataframe.columns.values:
        if str(dataframe.dtypes[col]).startswith("float"):
            if col in _WELL_KNOWN_SPATIAL_COLUMN_NAMES.keys():
                guess_spatial_names.append(col)
            else:
                guess_continuous_names.append(col)
        elif str(dataframe.dtypes[col]).startswith("datetime"):
                guess_spatial_names.append(col)
        elif str(dataframe.dtypes[col]).startswith("int"):
            if col in _WELL_KNOWN_SAMPLE_INDEX_COLUMN_NAMES:
                guess_sample_index_names.append(col)
            else:
                guess_discrete_names.append(col)
        elif col not in _WELL_KNOWN_SAMPLE_INDEX_COLUMN_NAMES and (str(dataframe.dtypes[col]).startswith("object") or isinstance(dataframe.dtypes[col], pd.CategoricalDtype)):
            if dataset_column_name is None:
                if col == DATASET_DIMENSION_NAME:
                    guess_dataset_column_name = DATASET_DIMENSION_NAME
                else:
                    guess_discrete_names.append(col)
            elif col != dataset_column_name:
                guess_discrete_names.append(col)

    if continuous_column_names is None:
        continuous_column_names = guess_continuous_names
        continuous_column_names += guess_spatial_names

    if discrete_column_names is None:
        discrete_column_names = guess_discrete_names

    if sample_index_column_names is None:
        sample_index_column_names = []
        for name in _WELL_KNOWN_SAMPLE_INDEX_COLUMN_NAMES:
            if name in guess_sample_index_names:
                sample_index_column_names.append(name)

    if dataset_column_name is None:
        dataset_column_name = guess_dataset_column_name

    logger.info(f"Using continuous columns  : {continuous_column_names}")
    logger.info(f"Using discrete columns    : {discrete_column_names}")
    logger.info(f"Using sample index columns: {sample_index_column_names}")
    logger.info(f"Using dataset column      : {dataset_column_name}")

    epoch_timestamp: pd.Timestamp = None

    continuous_dimensions = []
    for col_name in continuous_column_names:
        col = dataframe[col_name]
        info = investigation_pb2.ContinuousDimensionInfo()
        info.name = col_name
        if col_name in _WELL_KNOWN_SPATIAL_COLUMN_NAMES.keys():
            info.type = _WELL_KNOWN_SPATIAL_COLUMN_NAMES[col_name]
        else:
            info.type = investigation_pb2.DimensionEnum.Continuous

        if info.type == investigation_pb2.DimensionEnum.Date:
            epoch_timestamp = dataframe[col_name].min()
            
        if continuous_column_info is not None:
            if col_name in continuous_column_info.keys():
                logger.info(f"Using continuous_column_info: {col_name}")
                property_info = continuous_column_info[col_name]
                if property_info.property_name:
                    info.property_name = property_info.property_name
                if property_info.unit_symbol:
                    info.display_units = property_info.unit_symbol
                info.default_is_logarithmic = property_info.is_logarithmic
                if property_info.min or property_info.max:
                    info.default_range.is_set = True
                    info.default_range.min = property_info.min
                    info.default_range.max = property_info.max
                    info.use_manual_range = True

        if not info.default_range.is_set:
            if info.type == investigation_pb2.DimensionEnum.Date:
                min_timestamp = _get_offset_from_date(epoch_timestamp, dataframe[col_name].min())
                max_timestamp = _get_offset_from_date(epoch_timestamp, dataframe[col_name].max())
                info.default_range.is_set = True
                info.default_range.min = min_timestamp
                info.default_range.max = max_timestamp
            else:
                info.default_range.is_set = True
                info.default_range.min = dataframe[col_name].min()
                info.default_range.max = dataframe[col_name].max()

        continuous_dimensions.append(info)

    discrete_dimensions = []
    discrete_lookup = {}
    if discrete_column_names is not None:
        for col_name in discrete_column_names:
            col = dataframe[col_name]
            unique = list(col.unique())
            discrete_lookup[col_name] = unique

            info = investigation_pb2.DiscreteDimensionInfo()
            info.name = col_name
            info.type = investigation_pb2.DimensionEnum.Discrete
            info.group.name = col_name
            options = []
            for index, val in enumerate(unique):
                option = investigation_pb2.DiscreteOption()
                option.option_name = str(val)
                option.value.index = index
                options.append(option)
            info.group.options.extend(options)
            discrete_dimensions.append(info)

    datasets = None
    if dataset_column_name is not None:
        datasets = list(dataframe[dataset_column_name].unique())

    if len(continuous_dimensions) == 0:
        raise ValueError("No continuous columns were selected from the dataframe")

    msg = investigator_api_pb2.InvestigationDefinition()
    if hasattr(dataframe, 'name'):
        msg.name = dataframe.name
    else:
        msg.name = f"Dataframe {str(id(dataframe))}"
    msg.continuous_dimensions.values.extend(continuous_dimensions)
    msg.discrete_dimensions.values.extend(discrete_dimensions)
    if epoch_timestamp is not None:
        timestamp = Timestamp()
        timestamp.FromDatetime(epoch_timestamp.to_pydatetime())
        msg.min_date.CopyFrom(timestamp)

    payload = Any()
    payload.Pack(msg)

    result = context.do_unary_request("investigator.CreateDataframeInvestigation", payload)
    if result[0]:
        response = investigator_api_pb2.InvestigationSummary()
        result[1].Unpack(response)
        investigation_id = response.id
    else:
        raise CegalHubError(result[1])

    logger.debug(f"Creating investigation: {investigation_id}")

    def payload_generator(dataset: str = None):
        count = 0
        payload_msg = investigator_api_pb2.UploadDataframeRowsCollection()
        payload_msg.investigation_id.id = investigation_id
        
        if dataset is None:
            df = dataframe
            payload_msg.data.parent_id = ""
            payload_msg.data.dataset_id = "Data"
        else:
            df = dataframe[dataframe[dataset_column_name] == dataset]
            parent_id = ""
            dataset_id = dataset
            if DATASET_FOLDER_SEPARATOR in dataset:
                split_index = dataset.index(DATASET_FOLDER_SEPARATOR)
                parent_id = dataset[:split_index]
                dataset_id = dataset[split_index+1:]

            payload_msg.data.parent_id = parent_id
            payload_msg.data.dataset_id = dataset_id

        def to_continuous_value(col_name, val):
            if col_name == DATE_SPATIAL_DIMENSION_NAME:
                return _get_offset_from_date(epoch_timestamp, val)
            return val

        for index, row in df.iterrows():
            count += 1

            msg = investigator_api_pb2.DataframeRow()
            msg.continuous_values.extend([to_continuous_value(col_name, row[col_name]) for col_name in continuous_column_names])

            if discrete_column_names is not None:
                msg.discrete_values.extend([discrete_lookup[col_name].index(row[col_name]) for col_name in discrete_column_names])

            if sample_index_column_names is not None:
                msg.sample_index.extend([int(row[col_name]) for col_name in sample_index_column_names])

            payload_msg.data.rows.extend([msg])

            if count >= _NUM_ROWS_PER_CHUNK:
                yield payload_msg
                count = 0
                payload_msg = investigator_api_pb2.UploadDataframeRowsCollection()
                payload_msg.investigation_id.id = investigation_id

        if count > 0:
            yield payload_msg

    if datasets is None:
        result = context.do_client_streaming("investigator.UploadDataframeRows", _pack_payloads(payload_generator()))
        if not result[0]:
            raise CegalHubError(result[1])
    else:
        for dataset in datasets:
            result = context.do_client_streaming("investigator.UploadDataframeRows", _pack_payloads(payload_generator(dataset)))
        if not result[0]:
            raise CegalHubError(result[1])

    return Investigation(context, investigation_id=investigation_id)
