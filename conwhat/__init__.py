
__all__ = [ 'VolTractAtlas', 'VolConnAtlas', 'StreamTractAtlas', 'StreamConnAtlas' ]

from .atlas import (VolTractAtlas,VolConnAtlas,
                   StreamTractAtlas,StreamConnAtlas)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
