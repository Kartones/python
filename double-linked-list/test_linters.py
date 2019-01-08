import subprocess
import sys


SOURCE_FOLDER = "."


def test_flake8_compliance() -> None:
    flake8_binary = subprocess.check_output("which flake8",
                                            shell=True,
                                            stderr=sys.stderr).decode("ascii").replace("\n", "")

    result = subprocess.call("{} {}".format(flake8_binary, SOURCE_FOLDER),
                             shell=True,
                             stdout=sys.stdout,
                             stderr=sys.stderr)
    assert result == 0


def test_mypy_compliance() -> None:
    mypy_binary = subprocess.check_output("which mypy",
                                          shell=True,
                                          stderr=sys.stderr).decode("ascii").replace("\n", "")

    result = subprocess.call("{} --config-file ../mypy.ini {}".format(mypy_binary, SOURCE_FOLDER),
                             shell=True,
                             stdout=sys.stdout,
                             stderr=sys.stderr)
    assert result == 0
