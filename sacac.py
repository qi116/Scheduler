from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("scheduling.py",compiler_directives={'language_level' : "3"}),name="s2"
)