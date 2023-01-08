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
        items = self._load_list_items_from_file(file_path)
        return self._get_items_data(items)

    def save_list_item_action(self, list_name, item_name, action):
        file_path = os.path.join(".", self.config.LISTS_FOLDER, "{}.txt".format(self._clean_list_name(list_name)))
        items = self._load_list_items_from_file(file_path)

        if action == "c":
            items[item_name] = "1"
        elif action == "u":
            items[item_name] = "0"
        elif action == "h":
            items[item_name] = "2"
        elif action == "d":
            if item_name in items:
                del items[item_name]

        self._save_list(list_name, items)

    def _save_list(self, list_name, list_items):
        separator = self.config.SEPARATOR
        file_path = os.path.join(".", self.config.LISTS_FOLDER, "{}.txt".format(self._clean_list_name(list_name)))
        if not os.path.exists(file_path):
            raise IOError("Invalid list")
        with open(file_path, "w") as file:
            file.write("\r\n".join(["{}{}{}".format(name, separator, state) for name, state in list_items.items()]))

    @staticmethod
    def _get_txt_files_from_directory(path):
        return [filename for filename in os.listdir(path) if filename.endswith(".txt")]

    @staticmethod
    def _get_list_name(filepath):
        return filepath.split(".")[0]

    def _load_list_items_from_file(self, filepath):
        separator = self.config.SEPARATOR

        with open(filepath, "r") as file:
            items = {line.split(separator)[0]: line.split(separator)[1].replace("\n", "") for line in file}
        return items

    @classmethod
    def _get_items_data(cls, items_dict):
        data = []
        for item_name in sorted(items_dict.keys()):
            fragments = [item_name, items_dict[item_name]]
            fragments.append(cls._css_class_for_item(items_dict[item_name]))
            data.append(fragments)
        return data

    @staticmethod
    def _clean_list_name(list_name):
        return re.sub(r"[\/\\\.]", "", list_name)

    # TODO: Should go on a decorator outside of the service
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
