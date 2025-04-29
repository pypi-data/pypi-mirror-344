# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""The cegalprizm.investigator module provides the API to allow Blueback Investigations to be accessed from Python.
"""

__version__ = '1.4.0'
__git_hash__ = '44935bf5'

import logging
logger = logging.getLogger(__name__)

# pylint: disable=wrong-import-position

from .constants import *
from .connection import InvestigatorConnection
from .config import Config
from .decorators import InvestigatorPyFunction1D
from .decorators import InvestigatorPyFunction2D
from .named_tuples import *
from .pickling import *
from .petrel import PetrelInvestigation
from .plotting import *
from .statistics import *
from .utils_investigation import *
from .utils_pythontoolpro import *
from .views import *

from .inv.investigation import Investigation

