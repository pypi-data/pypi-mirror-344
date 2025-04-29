import sys
from pathlib import Path

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

import shared_ndarray2


def test_version():
    pyproj_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproj_path, "rb") as pyproj_f:
        config = tomllib.load(pyproj_f)
    assert config["project"]["version"] == shared_ndarray2.__version__
