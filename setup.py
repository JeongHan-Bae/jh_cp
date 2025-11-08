import os
import sys
from setuptools import setup, find_packages

"""
📦 Load project metadata from pyproject.toml
"""
__setup_dir__ = os.path.dirname(os.path.abspath(__file__))
__pyproject_path__ = os.path.join(__setup_dir__, "pyproject.toml")

# tomllib is built-in from Python 3.11+, fallback to tomli for 3.10
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

with open(__pyproject_path__, "rb") as f:
    pyproject_data = tomllib.load(f)

project = pyproject_data.get("project", {})
build_system = pyproject_data.get("build-system", {})

# Extract metadata
__package_name__ = project.get("name", "unknown-package")
__version__ = project.get("version", "0.0.0")
__description__ = project.get("description", "")
__author__ = project.get("authors", [{}])[0].get("name", "")
__author_email__ = project.get("authors", [{}])[0].get("email", "")
__url__ = project.get("urls", {}).get("Homepage", "")

"""
📖 Long description (from README.md)
"""
with open(os.path.join(__setup_dir__, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

"""
🏗️ Setup configuration
"""
setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__url__,
    license="Apache License 2.0",

    python_requires=project.get("requires-python", ">=3.9"),
    packages=find_packages(include=["jh_cp", "jh_cp.*"]),
    include_package_data=True,
    package_data={
        "jh_cp.jh_cp_tools": [".cp_ignore", "exclude-rules.ini"],
    },

    entry_points={
        "console_scripts": [
            # use same script name defined in pyproject.toml for consistency
            "jh_cp = jh_cp.jh_cp:jh_cp_main",
        ],
    },

    classifiers=project.get("classifiers", []),
)
