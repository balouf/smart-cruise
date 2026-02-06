"""Top-level package for Smart Cruise."""

from importlib.metadata import metadata
from smart_cruise.models import CostModel as CostModel
from smart_cruise.models import CostRandom as CostRandom
from smart_cruise.smart_cruise import Cruise as Cruise

infos = metadata(__name__)
__version__ = infos["Version"]
__author__ = "Fabien Mathieu"
__email__ = "fabien.mathieu@normalesup.org"
