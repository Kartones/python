import csv
import gzip
import os
import requests
import shutil
from typing import Dict, List


class Fetch():
    """
    Info: https://www.imdb.com/interfaces/
    """

    IMDB_DATASETS_URL = "https://datasets.imdbws.com/"

    TITLES_DATASET_NAME = "title.basics.tsv.gz"
    TITLES_DATASET_FILE = "title.basics.tsv"
    """
        relevant fields:
            0: tconst -> id
            1: titleType -> filter to "movie"
    """

    RATINGS_DATASET_NAME = "title.ratings.tsv.gz"
    RATINGS_DATASET_FILE = "title.ratings.tsv"
    """
        relevant fields:
            0: tconst -> id
            1: averageRating -> float
    """

    # Note: doesn't includes header row
    OUTPUT_FILE = "imdb-titles.csv"

    @classmethod
    def run(cls) -> None:
        compressed_datasets = [cls.RATINGS_DATASET_NAME, cls.TITLES_DATASET_NAME]
        cls._fetch_and_save(compressed_datasets)
        cls._extract(compressed_datasets)

        cls._transform()

        print("> Finished")

    @classmethod
    def _fetch_and_save(cls, datasets: List[str]) -> None:
        for dataset in datasets:
            print("> Fetching {}".format(dataset))
            response = requests.get("{}{}".format(cls.IMDB_DATASETS_URL, dataset))

            print("> Saving {}".format(dataset))
            with open(dataset, "wb") as file_handle:
                file_handle.write(response.content)

            print("> Written {} to file".format(dataset))

    @classmethod
    def _extract(cls, datasets: List[str]) -> None:
        for compressed_file in datasets:
            destination_name = compressed_file[:compressed_file.rindex(".gz")]

            print("> Extracting {}".format(compressed_file))
            with gzip.open(compressed_file, "rb") as gzip_file_handle:
                with open(destination_name, "wb") as output_file_handle:
                    shutil.copyfileobj(gzip_file_handle, output_file_handle)

            print("> Deleting compressed file {}".format(compressed_file))
            os.remove(compressed_file)

    @classmethod
    def _transform(cls, ) -> None:
        movie_ratings = dict()  # type: Dict[str, float]

        print("> Reading {}".format(cls.RATINGS_DATASET_FILE))
        with open(cls.RATINGS_DATASET_FILE, "r") as ratings_file_handle:
            tsv_reader = csv.reader(ratings_file_handle, delimiter="\t")

            # Skip header line
            next(ratings_file_handle)
            for row in tsv_reader:
                movie_ratings[row[0]] = float(row[1])

        print("> Reading {}".format(cls.TITLES_DATASET_FILE))
        with open(cls.TITLES_DATASET_FILE, "r") as titles_file_handle, open(cls.OUTPUT_FILE, "w") as output_file_handle:
            tsv_reader = csv.reader(titles_file_handle, delimiter="\t")
            csv_writer = csv.writer(output_file_handle, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)

            # Skip header line
            next(titles_file_handle)
            for row in tsv_reader:
                if (row[1] == "movie"):
                    csv_writer.writerow([row[2], movie_ratings.get(row[0], "")])

        print("> Written {}".format(cls.OUTPUT_FILE))


if __name__ == "__main__":
    fetch = Fetch()
    fetch.run()
