"""test the installation"""
from casymda import __version__


def test_version():
    """version should not be none"""
    assert __version__ is not None
