#!/usr/bin/python
# -!- coding: utf-8 -!-

import os
import re


class ShoppingLists():

    def __init__(self, config):
        self.config = config

    def get_all_lists(self):
        folder_path = os.path.join(".", self.config.LISTS_FOLDER)
        files = self._get_txt_files_from_directory(folder_path)
        return [self._get_list_name(file) for file in sorted(files)]

    def get_items(self, list_name):
        file_path = os.path.join(".", self.config.LISTS_FOLDER, "{}.txt".format(self._clean_list_name(list_name)))
        items = self._get_items_from_file(file_path)
        return self._get_items_data(items)

    def save_list(self, list_name, list_items):
        file_path = os.path.join(".", self.config.LISTS_FOLDER, "{}.txt".format(self._clean_list_name(list_name)))
        if not os.path.exists(file_path):
            raise IOError("Invalid list")
        with open(file_path, "w") as file:
            file.write("\r\n".join(list_items))

    @staticmethod
    def _get_txt_files_from_directory(path):
        return [filename for filename in os.listdir(path) if filename.endswith(".txt")]

    @staticmethod
    def _get_list_name(filepath):
        return filepath.split(".")[0]

    @staticmethod
    def _get_items_from_file(filepath):
        with open(filepath, "r") as file:
            items = file.readlines()
        return items

    @classmethod
    def _get_items_data(cls, items_list):
        data = []
        for item in sorted(items_list):
            fragments = item.replace("\n", "").rsplit(" ", maxsplit=1)
            fragments.append(cls._css_class_for_item(fragments[1]))
            data.append(fragments)
        return data

    @staticmethod
    def _clean_list_name(list_name):
        return re.sub(r"[\/\\\.]", "", list_name)

    # Should go on a decorator outside of the service, but I'm lazy
    @staticmethod
    def _css_class_for_item(item_status):
        css_class = ""
        if item_status == "0":
            css_class = "btn-default"
        elif item_status == "1":
            css_class = "btn-warning"
        elif item_status == "2":
            css_class = "btn-danger"

        return css_class
