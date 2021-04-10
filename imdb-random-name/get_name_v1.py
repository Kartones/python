import csv
from random import randint
import subprocess
import sys


class NameChooser():
    """
        One-off approach to simply return a movie name
    """

    TITLES_FILE = "imdb-titles.csv"

    @classmethod
    def choose_one(cls) -> str:
        num_titles = cls._count_number_of_titles()

        if (num_titles == 0):
            print("> Couldn't count titles from {}".format(cls.TITLES_FILE))
            exit(1)

        chosen_number = randint(0, num_titles - 1)

        with open(cls.TITLES_FILE, "r") as titles_file_handle:
            csv_reader = csv.reader(titles_file_handle)

            for index, row in enumerate(csv_reader):
                if (index == chosen_number):
                    return row[0]

        return "> No title returned"

    @classmethod
    def _count_number_of_titles(cls) -> int:
        output = ""

        result = subprocess.run(
            "wc -l {}".format(cls.TITLES_FILE),
            shell=True,
            capture_output=True,
        )

        assert result.returncode == 0

        try:
            return int(result.stdout.decode("UTF-8").strip().split(" ")[0])
        except Exception:
            return 0


if __name__ == "__main__":
    name_chooser = NameChooser()

    print(name_chooser.choose_one())
