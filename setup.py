from distutils.core import setup, find_packages
import distutils.text_file
from pathlib import Path
from typing import List

def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()


setup(
    name='srabuilder',
    version='0.0.1',
    packages=find_packages(),
    install_requires=_parse_requirements('requirements.txt'),
    license='MIT',
    long_description='placeholder',
)