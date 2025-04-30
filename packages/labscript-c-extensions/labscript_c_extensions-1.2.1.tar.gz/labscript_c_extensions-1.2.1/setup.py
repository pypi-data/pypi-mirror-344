import os
from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext


CMDCLASS = {"build_ext": build_ext}

EXT_MODULES = [
    Extension(
        "labscript_c_extensions.runviewer.resample",
        sources=[os.path.join("src", "runviewer", "resample.pyx")],
    )
]

setup(
    cmdclass=CMDCLASS,
    ext_modules=EXT_MODULES,
)
