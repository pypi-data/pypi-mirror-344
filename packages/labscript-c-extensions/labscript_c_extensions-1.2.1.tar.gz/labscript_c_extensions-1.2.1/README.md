<img src="https://raw.githubusercontent.com/labscript-suite/labscript-suite/master/art/labscript_32nx32n.svg" height="64" alt="the labscript suite" align="right">

# the _labscript suite_ » labscript-c-extensions

### C language extensions used by the _labscript suite_

[![Actions Status](https://github.com/labscript-suite/labscript-c-extensions/workflows/Build%20and%20Release/badge.svg)](https://github.com/labscript-suite/labscript-c-extensions/actions)
[![License](https://img.shields.io/pypi/l/labscript-c-extensions.svg)](https://github.com/labscript-suite/labscript-c-extensions/raw/master/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/labscript-c-extensions.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/labscript-c-extensions.svg)](https://pypi.org/project/labscript-c-extensions)
[![Conda Version](https://img.shields.io/conda/v/labscript-suite/labscript-c-extensions)](https://anaconda.org/labscript-suite/labscript-c-extensions)
[![Conda Platforms](https://img.shields.io/conda/pn/labscript-suite/labscript-c-extensions)](https://anaconda.org/labscript-suite/labscript-c-extensions)
[![Google Group](https://img.shields.io/badge/Google%20Group-labscriptsuite-blue.svg)](https://groups.google.com/forum/#!forum/labscriptsuite)
<!-- [![DOI](http://img.shields.io/badge/DOI-10.1063%2F1.4817213-0F79D0.svg)](https://doi.org/10.1063/1.4817213) -->


C language extensions used by the [*labscript suite*](https://github.com/labscript-suite/labscript-suite). We provide built distributions for these extensions as conda packages on [Anaconda Cloud](https://anaconda.org/labscript-suite/labscript-c-extensions) and wheels on [PyPI](https://pypi.org/project/labscript-c-extensions/#files) for various platforms.

Bundling these extensions in a separate module ensures that developer installations of other _labscript suite_ components don't depend on build tools, as they can install the prebuilt wheel/conda package containing the extensions. Only developers of these extensions need the build tools (for example, [MSVC++ on Windows](https://wiki.python.org/moin/WindowsCompilers))


## Installation

labscript-c-extensions is distributed as a Python package on [PyPI](https://pypi.org/user/labscript-suite) and [Anaconda Cloud](https://anaconda.org/labscript-suite), and should be installed with other components of the _labscript suite_. Please see the [installation guide](https://docs.labscriptsuite.org/en/latest/installation) for details.
