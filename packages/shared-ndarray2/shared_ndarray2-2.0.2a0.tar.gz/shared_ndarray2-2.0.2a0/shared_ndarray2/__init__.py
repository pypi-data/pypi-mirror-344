"""shared_ndarray2 - Provides the SharedNDArray class that streamlines the use of NumPy ndarrays with
multiprocessing.shared_memory.
"""

from .shared_ndarray import (
    VALID_SHARED_TYPES as VALID_SHARED_TYPES,
)
from .shared_ndarray import (
    ShareableT as ShareableT,
)
from .shared_ndarray import (
    SharedNDArray as SharedNDArray,
)
from .version import __version__
