import subprocess
import sys

from flake8.api import legacy as flake8


def test_flake8_compliance() -> None:
    pep8style = flake8.get_style_guide(config_file=".flake8")
    result = pep8style.check_files(["."])
    assert result.total_errors == 0


def test_mypy_compliance() -> None:
    result = subprocess.call("/usr/local/bin/mypy --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
                             " --warn-redundant-casts --warn-return-any"
                             " --warn-unused-ignores --strict-optional .",
                             shell=True,
                             stdout=sys.stdout,
                             stderr=sys.stderr)
    assert result == 0
