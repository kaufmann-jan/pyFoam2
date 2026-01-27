import pyFoam2


def test_version_defined():
    assert hasattr(pyFoam2, "__version__")
    assert isinstance(pyFoam2.__version__, str)
    assert pyFoam2.__version__
