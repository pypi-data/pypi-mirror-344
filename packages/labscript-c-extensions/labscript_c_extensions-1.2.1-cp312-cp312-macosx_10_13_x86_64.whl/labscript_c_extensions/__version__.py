#####################################################################
#                                                                   #
# /__version__.py                                                   #
#                                                                   #
# Copyright 2013, Monash University                                 #
#                                                                   #
# This file is part of the program labscript-c-extensions, in the   #
# labscript suite (see http://labscriptsuite.org), and is licensed  #
# under the Simplified BSD License. See the license.txt file in the #
# root of the project for the full license.                         #
#                                                                   #
#####################################################################
from pathlib import Path
try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata

root = Path(__file__).parent.parent
if (root / '.git').is_dir():
    try:
        from setuptools_scm import get_version
        VERSION_SCHEME = {
            "version_scheme": "guess-next-dev",
            "local_scheme": "node-and-date",
        }
        scm_version = get_version(root, **VERSION_SCHEME)
    except ImportError:
        scm_version = None
else:
    scm_version = None

if scm_version is not None:
    __version__ = scm_version
else:
    try:
        __version__ = importlib_metadata.version(__package__)
    except importlib_metadata.PackageNotFoundError:
        __version__ = None
