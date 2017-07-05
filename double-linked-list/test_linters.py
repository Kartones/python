import subprocess
import sys


def test_flake8_compliance() -> None:
    result = subprocess.call("/usr/local/bin/flake8 .",
                             shell=True,
                             stdout=sys.stdout,
                             stderr=sys.stderr)
    assert result == 0


def test_mypy_compliance() -> None:
    result = subprocess.call("/usr/local/bin/mypy --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
                             " --warn-redundant-casts --warn-return-any"
                             " --warn-unused-ignores --strict-optional .",
                             shell=True,
                             stdout=sys.stdout,
                             stderr=sys.stderr)
    assert result == 0
