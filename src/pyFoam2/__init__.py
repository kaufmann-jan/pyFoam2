"""Utility-classes for OpenFOAM."""

from pyFoam2.infrastructure.configuration import Configuration

__all__ = [
    "__version__",
    "version",
    "versionString",
    "foamVersionString",
    "configuration",
]

__version__ = "0.1.6"


def version():
    """:return: Version number as a tuple"""
    parts = []
    for token in __version__.replace("-", ".").split("."):
        try:
            parts.append(int(token))
        except ValueError:
            parts.append(token)
    return tuple(parts)


def versionString():
    """:return: Version number of pyFoam2"""
    v = version()

    v_str = "%d" % v[0] if v else "0"
    for d in v[1:]:
        if type(d) == int:
            v_str += (".%d" % d)
        else:
            v_str += ("-%s" % str(d))
    return v_str


def foamVersionString():
    from pyFoam2.foam_information import foamVersionString

    return foamVersionString()


_configuration = Configuration()


def configuration():
    """:return: The Configuration information of pyFoam2"""
    return _configuration
