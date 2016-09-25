#!/usr/bin/python
# coding: utf-8

import re
import sys
import hashlib
from os import listdir
from os.path import isfile, join


# Input files are generated with:
# du -ac /media/kartones/<volume-name>/ > <filename>.txt
class ListSearch():

    def search(self, text):
        text = text.strip().lower()
        print("> Searching for '{}'".format(text))

        contents = []
        files_in_dir = self._get_txt_files_from_directory()
        for file in files_in_dir:
            contents = contents + self._read_file(file)

        self._search_and_print(text, contents)
        self._search_and_print(text.replace(" ", "_"), contents)
        self._search_and_print(text.replace(" ", "."), contents)
        self._search_and_print(text.replace(" ", "-"), contents)

    def _search_and_print(self, text, contents):
        ocurrences = self._find_ocurrences(text, contents)
        for result in ocurrences:
            print("  {}".format(result["str"]))

    def _find_ocurrences(self, text, content):
        original_ocurrences = [line for line in content if text in line]
        ocurrences = []

        for line in original_ocurrences:
            # Clear folder/file size and starting garbage
            result = {
                "str": re.sub(r"^(.*)/media/kartones/", "", line)
            }
            # Add position of text match
            result["pos"] = result["str"].find(text)
            # Calculate hash of contents before text match (to detect same folder results)
            hash_lib = hashlib.md5()
            hash_lib.update(bytes(result["str"][:result["pos"]], "utf-8"))
            result["prefix_hash"] = hash_lib.digest()
            ocurrences.append(result)

        # Now make a map to keep just one ocurrence per same result
        ocurrences_map = {ocurrence["prefix_hash"]: ocurrence for ocurrence in ocurrences}

        return ocurrences_map.values()

    def _read_file(self, filename):
        return [line.strip().lower() for line in open(filename)]

    def _get_txt_files_from_directory(self, path="."):
        return \
            [filename for filename in listdir(path) if filename.endswith(".txt") and isfile(join(path, filename))]


# Main
# ----

if len(sys.argv) < 2:
    exit(1)

text_to_search = " ".join(sys.argv[1:])

list_search = ListSearch()
list_search.search(text_to_search)
