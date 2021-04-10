import csv
from random import randint
import subprocess
import sys
from typing import List, Optional


class NameChooser():
    """
        Alternative approach to support filtering by rating (upon load) and by starting letter
    """

    TITLES_FILE = "imdb-titles.csv"

    def __init__(self, rating_filter_gt: float = 0.0) -> None:
        self.movies = list()  # type: List[str]

        self._load_movies(rating_filter_gt)

    # Optimization: directly don't add those below filter
    def choose_one(self, first_letter_filter: Optional[str] = None) -> str:
        if first_letter_filter:
            filtered_movies = [
                movie for movie in self.movies
                if movie.startswith(first_letter_filter) or movie.startswith(first_letter_filter.upper())
            ]
            num_titles = len(filtered_movies)
            chosen_number = randint(0, num_titles - 1)
            return filtered_movies[chosen_number]
        else:
            num_titles = len(self.movies)
            chosen_number = randint(0, num_titles - 1)
            return self.movies[chosen_number]

    def _load_movies(self, rating_filter_gt: float = 0.0) -> None:
        with open(self.TITLES_FILE, "r") as titles_file_handle:
            csv_reader = csv.reader(titles_file_handle)

            for row in csv_reader:
                rating = float(row[1] or 0)
                if rating >= rating_filter_gt:
                    self.movies.append(row[0])

        if len(self.movies) == 0:
            print("> Error: no movies loaded. Maybe rating filter is wrong? (value: {})".format(rating_filter_gt))
            exit(1)


if __name__ == "__main__":
    rating_filter = 0.0
    if len(sys.argv) > 1:
        try:
            rating_filter = float(sys.argv[1])
        except ValueError:
            pass

    first_letter_filter = None
    if len(sys.argv) > 2:
        first_letter_filter = sys.argv[2].lower() if len(sys.argv[2]) == 1 else None

    name_chooser = NameChooser(rating_filter_gt=rating_filter)

    print(name_chooser.choose_one(first_letter_filter=first_letter_filter))
