from distutils.core import setup
from setuptools import find_packages
import distutils.text_file
import sys
from pathlib import Path
from typing import List

def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()

install_requires= [
    "dfly-breathe",
    "sounddevice",
    "dragonfly[kaldi]",
    "webrtcvad-wheels == 2.0.*"
]

setup(
    name='srabuilder',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    license='MIT',
    long_description='placeholder',
)