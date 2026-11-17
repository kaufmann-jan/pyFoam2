from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from pyFoam2.run_dictionary import ParsedParameterFile
from pyFoam2.run_dictionary.parsed_parameter_file import PyFoamParserError


def check_headerless_waves_dictionary_round_trip(tmp_path):
    source = tmp_path / 'wavesDict'
    source.write_text(
        '/* FoamFile { class dictionary; } */\n'
        '// Wave definitions\n'
        'Stokes5\n{ amplitude 0.3; depth 30.0; length 40.0; }\n'
    )
    parsed = ParsedParameterFile(str(source))
    assert parsed.noHeader is True
    assert parsed.header is None
    assert parsed['Stokes5']['amplitude'] == 0.3
    parsed.writeFile()
    reread = ParsedParameterFile(str(source))
    assert reread.header is None
    assert reread['Stokes5']['length'] == 40.0


def check_headered_dictionary(tmp_path):
    source = tmp_path / 'dictionary'
    source.write_text(
        '/* Banner */\nFoamFile { class dictionary; format ascii; }\n'
        'amplitude 0.3;\n'
    )
    parsed = ParsedParameterFile(str(source))
    assert parsed.noHeader is False
    assert parsed.header['class'] == 'dictionary'
    assert parsed['amplitude'] == 0.3


def check_explicit_header_requirement(tmp_path):
    source = tmp_path / 'wavesDict'
    source.write_text('Stokes5 { amplitude 0.3; }\n')
    with TestCase().assertRaises(PyFoamParserError):
        ParsedParameterFile(str(source), noHeader=False)


class TestHeaderDetection(TestCase):
    def test_headerless_round_trip(self):
        with TemporaryDirectory() as directory:
            check_headerless_waves_dictionary_round_trip(Path(directory))

    def test_headered_dictionary(self):
        with TemporaryDirectory() as directory:
            check_headered_dictionary(Path(directory))

    def test_explicit_header_requirement(self):
        with TemporaryDirectory() as directory:
            check_explicit_header_requirement(Path(directory))
