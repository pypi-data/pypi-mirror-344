"""
DeepMIMO Python Package.
"""

__version__ = "4.0.0a3"

# Core functionality
from .generator.core import (
    generate,
    load,
)
from .generator.dataset import Dataset

# TX/RX handling
from .txrx import (
    TxRxSet,
    TxRxPair,
    get_txrx_sets,
    get_txrx_pairs,
    print_available_txrx_pair_ids,
)

# Visualization
from .generator.visualization import (
    plot_coverage,
    plot_rays,
    plot_power_discarding,
)

# Utilities
from .generator.generator_utils import (
    get_idxs_with_limits,
    LinearPath,
)

from .generator.geometry import (
    steering_vec,
)

# Channel parameters
from .generator.channel import ChannelGenParameters

from .converter.converter import convert
from .info import info
from .general_utils import (
    get_available_scenarios,
    get_params_path,
    load_dict_from_json,
    zip,
    get_scenario_folder,
)

from .summary import summary, plot_summary

from .api import (
    upload,
    upload_rt_source,
    download,
    search,
    upload_images,
)

# Physical world representation
from .scene import (
    Face,
    PhysicalElement,
    PhysicalElementGroup,
    Scene
)

# Import immediate modules
from . import consts
from . import general_utils

# Import the config instance
from .config import config

__all__ = [
    # Core functionality
    'generate',
    'convert', 
    'info',
    'load',
    'Dataset',
    'ChannelGenParameters',
    
    # TX/RX handling
    'TxRxSet',
    'TxRxPair',
    'get_txrx_sets',
    'get_txrx_pairs',
    'print_available_txrx_pair_ids',
    
    # Visualization
    'plot_coverage',
    'plot_rays',
    
    # Utilities
    'LinearPath',
    'get_idxs_with_limits',
    
    # Physical world representation
    'Face',
    'PhysicalElement',
    'PhysicalElementGroup',
    'Scene',
    
    # General utilities
    'summary',
    'upload',
    'upload_rt_source',
    'upload_images',
    'download',
    'search',
    'get_available_scenarios',
    'get_params_path',
    'load_dict_from_json',
    
    # Constants and configuration
    'consts',
    'general_utils',
    'config',
]
