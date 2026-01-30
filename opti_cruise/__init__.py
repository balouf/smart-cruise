"""Top-level package for Optimal Cruise Computation."""

from importlib.metadata import metadata
from opti_cruise.models import CostModel as CostModel
from opti_cruise.models import CostRandom as CostRandom
from opti_cruise.opti_cruise import Cruise as Cruise

infos = metadata(__name__)
__version__ = infos["Version"]
__author__ = "Fabien Mathieu"
__email__ = "fabien.mathieu@normalesup.org"
