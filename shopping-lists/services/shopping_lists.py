#!/usr/bin/python
# -!- coding: utf-8 -!-

import os


class ShoppingLists():

    def __init__(self, config):
        self.config = config

    def get_all_lists(self):
        folder_path = os.path.join(".", self.config.LISTS_FOLDER)
        files = self._get_txt_files_from_directory(folder_path)
        return [self._get_list_name(file) for file in sorted(files)]

    def get_items(self, list_name):
        file_path = os.path.join(".", self.config.LISTS_FOLDER, "{}.txt".format(list_name))
        items = self._get_items_from_file(file_path)
        return self._get_items_data(items)

    def save_list(self, list_name, list_items):
        file_path = os.path.join(".", self.config.LISTS_FOLDER, "{}.txt".format(list_name))
        if not os.path.exists(file_path):
            raise IOError("Invalid list")
        with open(file_path, "w") as file:
            file.write("\r\n".join(list_items))

    def _get_txt_files_from_directory(self, path):
        return [filename for filename in os.listdir(path) if filename.endswith(".txt")]

    def _get_list_name(self, filepath):
        return filepath.split(".")[0]

    def _get_items_from_file(self, filepath):
        with open(filepath, "r") as file:
            items = file.readlines()
        return items

    def _get_items_data(self, items_list):
        data = []
        for item in sorted(items_list):
            fragments = item.replace("\n", "").rsplit(" ", maxsplit=1)
            fragments.append(self._css_class_for_item(fragments[1]))
            data.append(fragments)
        return data

    # Should go on a decorator outside of the service, but I'm lazy
    def _css_class_for_item(self, item_status):
        css_class = ""
        if item_status == "0":
            css_class = "btn-default"
        elif item_status == "1":
            css_class = "btn-warning"
        elif item_status == "2":
            css_class = "btn-danger"

        return css_class
