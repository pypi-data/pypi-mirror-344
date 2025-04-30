from setuptools import setup, find_packages
import os
import re

# Read version from version.py without importing the package
with open(os.path.join('shanti', 'version.py'), 'r') as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string in version.py")


setup(
    name="shanti",
    version=version,
    description="create SHarable, interactive, stANdalone html dashboard from Tabular proteomIcs data",
    author="Nara Marella",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "bokeh",
        "openpyxl",
        "scipy",
        "numpy"
    ],
    include_package_data=True,
)
