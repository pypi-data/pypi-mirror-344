# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the Investigation class
"""

from typing import Callable, Dict, Iterable, List, Sequence, Tuple, Type, Union

import os.path

import pandas as pd

# pylint: disable=relative-beyond-top-level
# pylint: disable=import-outside-toplevel

from .. import logger
from ..constants import DATASET_DIMENSION_NAME, DATASET_FOLDER_SEPARATOR
from ..exceptions import CegalHubError
from ..hub_context import InvPyHubContext
from ..investigations import _get_available_investigations
from ..named_tuples import ContinuousPropertyTuple, DimensionPropertyNameTuple, DiscretePropertyTuple, DiscreteTagInfoTuple
from ..protos import investigation_pb2
from ..protos import investigator_api_pb2
from ..utils import _pack_payloads, _get_file_chunks, _get_dataset_geometry, _get_offset_from_date, _get_date_from_offset

from .continuous_dimension import ContinuousDimension
from .discrete_dimension import DiscreteDimension
from .discrete_dimension import _get_discrete_entries
from .dataset import Dataset

class InvestigationData:

    def _init(self):
        self._continuous_dimensions: investigator_api_pb2.ContinuousDimensionInfoCollection = None
        self._discrete_dimensions: investigator_api_pb2.DiscreteDimensionInfoCollection = None
        self._classification_groups: investigation_pb2.Classifications = None
        self._restrictions: investigation_pb2.Restrictions = None
        self._datasets: investigator_api_pb2.DatasetInfoCollection = None
        self._dataset_additional_discrete: list[Tuple[str, investigation_pb2.DiscreteGroup]] = None
        self._info: investigation_pb2.InvestigationInfo = None

class Investigation:
    """A class representing a Blueback Investigation

    The investigation object forms the entry point for all API access to a specific investigation.
    """

    def __init__(self,
                 context: InvPyHubContext,
                 path: str = None,
                 investigation_id: str = None):

        self._summary: investigator_api_pb2.InvestigationSummary = None
        self._hub_context: InvPyHubContext = context

        self._data: InvestigationData = None
        self._original: InvestigationData = None
        self._epoch_timestamp: pd.Timestamp = None

        if path and not os.path.exists(path):
            print(f"File '{path}'does not exist")
            return

        if path is not None:
            result = self._hub_context.do_client_streaming("investigator.UploadInvPyFile", _pack_payloads(_get_file_chunks(path)))
            if result[0]:
                response = investigator_api_pb2.InvestigationSummary()
                result[1].Unpack(response)
                self._summary = response
            else:
                raise CegalHubError(result[1])

        elif investigation_id is not None:
            for info in _get_available_investigations(self._hub_context):
                if self._summary is None and info.id == investigation_id:
                    self._summary = info

        if self._summary is None:
            logger.warning("Investigation cannot be accessed")
            return

        self._data = InvestigationData()
        self._original = InvestigationData()
        self.refresh()
        
        logger.info(f"Investigation: {self.id}")

    @property
    def is_valid(self) -> bool:
        """Is the investigation valid

        Returns:
            bool: The investigation validity
        """
        return self._summary is not None

    @property
    def id(self) -> str:
        """The identifier of this investigation

        Returns:
            str: The investigation identifier
        """
        return self._summary.id

    @property
    def name(self) -> str:
        """The name of this investigation

        Returns:
            str: The investigation name
        """
        return self._summary.name

    @property
    def num_continuous_dimensions(self) -> int:
        """The number of continuous dimensions

        Returns:
            int: The number of continuous dimensions
        """
        return len(self.continuous_dimension_names)

    @property
    def continuous_dimension_names(self) -> List[str]:
        """The names of the continuous dimensions

        Returns:
            list[str]: the names of the continuous dimensions
        """
        return [dimension.name for dimension in self._continuous_dimensions()]

    @property
    def continuous_dimension_property_names(self) -> List[DimensionPropertyNameTuple]:
        """A list of containing a tuple of continuous dimension name and the property name

        Returns:
            List[Tuple[str, str]]:  A list of tuples containing the dimension name and property name for each continuous dimension
        """
        return [DimensionPropertyNameTuple(dimension.name, dimension.property_name) for dimension in self._continuous_dimensions()]

    @property
    def num_discrete_dimensions(self) -> int:
        """The number of discrete dimensions

        Returns:
            int: The number of discrete dimensions
        """
        return len(self.discrete_dimension_names)

    @property
    def discrete_dimension_names(self) -> List[str]:
        """The names of the discrete dimensions

        Returns:
            list[str]: the names of the discrete dimensions
        """
        names = []
        if len(self.dataset_names) > 0:
            names.append(DATASET_DIMENSION_NAME)
        for dimension in self._discrete_dimensions():
            names.append(dimension.name)
        for classification_group in self._classification_groups():
            names.append(classification_group.name)
        for additional_discrete in self._dataset_additional_discrete():
            names.append(additional_discrete[1].name)
        return names

    @property
    def discrete_dimension_property_names(self) -> List[DimensionPropertyNameTuple]:
        """A list of containing a tuple of discrete dimension name and the property name

        Returns:
            List[Tuple[str, str]]:  A list of tuples containing the dimension name and property name for each discrete dimension
        """
        result = []
        if len(self.dataset_names) > 0:
            result.append(DimensionPropertyNameTuple(DATASET_DIMENSION_NAME, DATASET_DIMENSION_NAME))
        for dimension in self._discrete_dimensions():
            result.append(DimensionPropertyNameTuple(dimension.name, dimension.property_name))
        for classification_group in self._classification_groups():
            result.append(DimensionPropertyNameTuple(classification_group.name, classification_group.property_name))
        for additional_discrete in self._dataset_additional_discrete():
            result.append(DimensionPropertyNameTuple(additional_discrete[1].name, additional_discrete[1].property_name))
        return result

    @property
    def discrete_dimension_tags(self) -> Dict[str, List[str]]:
        """Returns a dictionary containing each discrete dimension name as a key
        and a list of the "tags" as the values

        Returns:
            Dict[str, List[str]]: A dictionary of dimension names and tags
        """
        result = {}
        for (key, value) in self._discrete_tuples().items():
            result[key] = [t[2] for t in value]
        return result

    @property
    def filter_names(self) -> List[str]:
        """The names of any filters

        Returns:
            list[str]: the names of any filters
        """
        names = []
        for restriction in self._restrictions():
            if investigation_pb2.RestrictionTypeEnum.Name(restriction.type) == 'Filter':
                names.append(restriction.name)
        return names

    @property
    def dataset_names(self) -> List[str]:
        """The names of the datasets

        Returns:
            list[str]: the names of the datasets
        """
        return [t[1] for t in self._datasets()]

    @property
    def dataset_geometries(self) -> List[Tuple[str, str]]:
        """The names and geometry types of the datasets

        The geometry type can be useful to determine the type of data from which the dataset contains 

        Returns:
            list[(str, str)]: a list of tuples containing the name and geometry type of each datasets
        """
        return [(t[1], t[2]) for t in self._datasets()]
    
    @property
    def available_units(self) -> Dict[str, List[str]]:
        """The available units for each continuous dimension

        Returns:
            Dict[str, list[str]]: a list of valid unit symbols for each continuous dimension name
        """
        return {dimension.name: dimension.available_units for dimension in self._continuous_dimensions()}

    @property
    def invariant_units(self) -> Dict[str, str]:
        """The invariant units for each continuous dimension

        Returns:
            Dict[str, str]: the invariant unit symbol for each continuous dimension name
        """
        return {dimension.name: dimension.invariant_units for dimension in self._continuous_dimensions()}

    @property
    def display_units(self) -> Dict[str, str]:
        """The display units for each continuous dimension

        Returns:
            Dict[str, str]: the display unit symbol for each continuous dimension name
        """
        return {dimension.name: dimension.display_units for dimension in self._continuous_dimensions()}

    @property
    def supported_plots(self) -> List[str]:
        """A list of the plot types in which this investigation can be shown

        Returns:
            List[str]: A list of strings describing the plot types in which this investigation can be shown
        """
        return [investigator_api_pb2._PLOTENUM.values[p.plot].name.lower() for p in self._summary.supported_plots if len(p.error_message) == 0]

    def _continuous_dimensions(self) -> Iterable[investigation_pb2.ContinuousDimensionInfo]:
        return self._data._continuous_dimensions.values
    
    def _discrete_dimensions(self) -> Iterable[investigation_pb2.DiscreteDimensionInfo]:
        return self._data._discrete_dimensions.values

    def _classification_groups(self) -> Iterable[investigation_pb2.ClassificationInfo]:
        return self._data._classification_groups.values

    def _restrictions(self) -> Iterable[investigation_pb2.Restriction]:
        return self._data._restrictions.values

    def _datasets(self) -> Iterable[Tuple[investigation_pb2.Dataset, str, str]]:
        return self._get_datasets(self._data._datasets)

    def _dataset_additional_discrete(self) -> Iterable[Tuple[str, investigation_pb2.DiscreteGroup]]:
        return self._data._dataset_additional_discrete

    def get_continuous_settings(self, name: str) -> ContinuousDimension:
        """Gets the continuous dimension settings for the specified dimension name

        Args:
            name (str): The name of the continuous dimension to be used

        Raises:
            ValueError: if the name is not a valid continuous dimension

        Returns:
            ContinuousDimension: The continuous dimension object
        """
        settings = next((x for x in self._continuous_dimensions() if x.name == name), None)
        if settings is None:
            raise ValueError(f"name ('{name}') must be one of {str(self.continuous_dimension_names)}")
        return ContinuousDimension(self, settings)

    def get_discrete_settings(self, name: str) -> DiscreteDimension:
        """Gets the discrete dimension settings for the specified dimension name

        Args:
            name (str): The name of the discrete dimension to be used

        Raises:
            ValueError: if the name is not a valid discrete dimension

        Returns:
            DiscreteDimension: The discrete discrete object
        """
        settings = next((x for x in self._discrete_dimensions() if x.name == name), None)
        if settings is None:
            settings = next((x for x in self._classification_groups() if x.name == name), None)
            if settings is None:
                raise ValueError(f"name ('{name}') must be one of {str(self.discrete_dimension_names)}")
            else:
                return None
        return DiscreteDimension(self, settings)

    def get_dataset_settings(self, name: str) -> Dataset:
        """Gets the settings for the specified dataset name

        Args:
            name (str): The name of the dataset to be used

        Raises:
            ValueError: if the name is not a valid dataset

        Returns:
            Dataset: The dataset object
        """
        settings = next((x[0] for x in self._datasets() if x[1] == name), None)
        if settings is None:
            raise ValueError(f"name ('{name}') must be one of {str(self.dataset_names)}")
        return Dataset(self, settings)

    def as_dataframe(self,
                     dataset_name: str = None,
                     continuous_columns: Union[str, Sequence[str]] = "all",
                     continuous_units: str = "display",
                     discrete_columns: Union[str, Sequence[str]] = "all",
                     discrete_data_as: str = "string",
                     include_filters: Union[str, Sequence[str]] = "all") -> pd.DataFrame:
        """A dataframe of all the points with both continuous and discrete dimensions

        Args:
            dataset_name (str, optional): The name of the dataset being output to the dataframe. Defaults to None.
            continuous_columns (Union[str, Sequence[str]], optional): Defaults to 'all'.
                                - 'all' will include all continuous dimensions from the investigation
                                - a list of continuous dimension names that should be included (see Investigation.continuous_dimension_names property)
                                - None which will include no continuous dimensions in the dataframe
            continuous_units (str, optional): Defaults to 'display'.
                                - 'display' will result in continuous values in invariant units
                                - 'invariant' will result in continuous values in invariant units
                                - a dictionary of continuous dimension names: a unit string (see Investigation.available_units property)
            discrete_columns (Union[str, Sequence[str]], optional): Defaults to 'all'.
                                - 'all' will include all discrete dimensions from the investigation
                                - a list of discrete dimension names that should be included (see Investigation.discrete_dimension_names property)
                                - None which will include no discrete dimensions in the dataframe
            discrete_data_as (str, optional): Defaults to 'string'.
                                - 'string' will cause discrete data tag to be returned as name
                                - 'value' will cause discrete data tag to be returned as int
            include_filters (Union[str, Sequence[str]], optional): Defaults to 'all'.
                                - 'all' will include all filters as boolean columns in the dataframe
                                - a list of filter names that should be included (see Investigation.filter_names property)
                                - None which will include no filter columns in the dataframe

        Raises:
            CegalHubError: if an unexpected error is reported by Hub

        Returns:
            pandas.DataFrame: A dataframe
        """
        from .to_dataframe import _to_dataframe

        return _to_dataframe(self,
                             dataset_name,
                             continuous_columns,
                             continuous_units,
                             discrete_columns,
                             discrete_data_as,
                             include_filters)

    def _get_datasets(self, dataset_collection, prefix: str = '') -> Iterable[Tuple[investigation_pb2.Dataset, str, str]]:
        for dataset in dataset_collection.values:
            if len(dataset.kids.values) == 0:
                yield tuple([dataset, prefix + dataset.name, _get_dataset_geometry(dataset.type)])
            else:
                yield tuple([dataset, prefix + dataset.name, _get_dataset_geometry(dataset.type)])
                for dataset_tuple in self._get_datasets(dataset.kids, prefix + dataset.name + DATASET_FOLDER_SEPARATOR):
                    yield dataset_tuple

    def _discrete_tuples(self) -> Dict[str, List[DiscreteTagInfoTuple]]:
        result = {}
        if len(self.dataset_names) > 0:
            result[DATASET_DIMENSION_NAME] = [DiscreteTagInfoTuple(index, t[0].id, t[1]) for index, t in enumerate(self._datasets())]
        for dimension in self._discrete_dimensions():
            result[dimension.name] = [DiscreteTagInfoTuple(t[1].value.index, t[1].id, t[0]) for t in _get_discrete_entries(dimension.group.options)]
        for classification_group in self._classification_groups():
            result[classification_group.name] = [DiscreteTagInfoTuple(entry.index, "", entry.name) for entry in classification_group.entries]
        for additional_discrete in self._dataset_additional_discrete():
            result[additional_discrete[1].name] = [DiscreteTagInfoTuple(tag.value.index, tag.id, tag.option_name) for tag in additional_discrete[1].options]
        return result

    def update(self):
        """Update the investigation with any recent changes

        Apply any recent changes to continuous/discrete dimensions or dataset settings to the investigation and therefore these changes will be visible when creating new plots etc

        Raises:
            CegalHubError: if an unexpected error is reported by Hub

        """
        from .update import _update_investigation
        _update_investigation(self)

    def refresh(self):
        """Refresh the investigation object

        This will fetch any changes made remotely to the investigation.
        It will override any local changes continuous/discrete dimensions or dataset settings that have not been applied by calling :func:update() method

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
        """
        from .refresh import _refresh
        _refresh(self)

    def reset(self):
        """Reset the investigation object

        This will reset any changes made remotely to the investigation.
        It will override any local changes continuous/discrete dimensions or dataset settings that have not been applied by calling :func:update() method

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
        """
        from copy import deepcopy
        from .update import _update_investigation
        from .refresh import _refresh
        self._data = deepcopy(self._original)
        _update_investigation(self)
        _refresh(self)

    def create_predictor(self, name: str, func: Callable, inputs: Sequence[ContinuousPropertyTuple], output: ContinuousPropertyTuple):
        """Create a new prediction equation in the investigation

        A new python prediction equation will be created in the investigation.
        Predictions will be made by invoking the provided func.

        Args:
            name (str): The name of the prediction to be used
            func (Callable): The function that performs the prediction
            inputs (Sequence[ContinuousPropertyTuple]):  a list of tuples each containing a continuous dimension name and a unit string
            output (ContinuousPropertyTuple): a tuple of continuous dimension name and a unit string

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
            ValueError: if any of the inputs are not valid
        """
        from .models import _save_predictor
        _save_predictor(self, name, func, inputs, output)

    def create_classifier(self, name: str, func: Callable, inputs: Sequence[ContinuousPropertyTuple], output: DiscretePropertyTuple):
        """Create a new classification equation in the investigation

        A new python classification equation will be created in the investigation.
        Classifications will be made by invoking the provided func.

        Args:
            name (str): The name of the classification to be used
            func (Callable): The function that performs the classification
            inputs (Sequence[ContinuousPropertyTuple]): a list of tuples each containing a continuous dimension name and a unit string
            output (DiscretePropertyTuple): a tuple of discrete name and a list of discrete tags

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
            ValueError: if any of the inputs are not valid
        """
        from .models import _save_classifier
        _save_classifier(self, name, func, inputs, output)


    def create_borehole_intersections(self, grid_names: Sequence[str]):
        """Force creation of the borehole intersection datasets for the defined grid names.

        Args:
            grid_names (Sequence[str]): The names of the grids to be used
        """
        if grid_names is None:
            raise ValueError("grid_names must be defined")
        if not isinstance(grid_names, list):
            raise ValueError("grid_names must be a list of strings")
        if len(grid_names) == 0:
            raise ValueError("grid_names must contain at least 1 entry")
        for name in grid_names:
            if name not in self.dataset_names:
                raise ValueError(f"{name} is not a valid, must be one of {str(self.dataset_names)}")

        from .intersections import _create_borehole_intersections
        _create_borehole_intersections(self, grid_names)

    def create_map_intersections(self, grid_names: Sequence[str]):
        """Force creation of the map intersection datasets for the defined grid names.

        Args:
            grid_names (Sequence[str]): The names of the grids to be used
        """
        if grid_names is None:
            raise ValueError("grid_names must be defined")
        if not isinstance(grid_names, list):
            raise ValueError("grid_names must be a list of strings")
        if len(grid_names) == 0:
            raise ValueError("grid_names must contain at least 1 entry")
        for name in grid_names:
            if name not in self.dataset_names:
                raise ValueError(f"{name} is not a valid, must be one of {str(self.dataset_names)}")
            
        from .intersections import _create_map_intersections
        _create_map_intersections(self, grid_names)
   
    def _get_offset_from_date(self, timestamp: pd.Timestamp) -> float:
        return _get_offset_from_date(self._epoch_timestamp, timestamp)

    def _get_date_from_offset(self, offset) -> pd.Timestamp:
        return _get_date_from_offset(self._epoch_timestamp, offset)
    