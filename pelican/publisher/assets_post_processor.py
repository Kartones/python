# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from shutil import copyfile, rmtree


class AssetPostProcessor(object):

    def __init__(self, config):
        self.config = config

    def create_duplicates(self, output_path):
        for source, destination in self.config.FILES_TO_DUPLICATE:
            source_filepath = "{}{}".format(output_path, source)
            destination_filepath = "{}{}".format(output_path, destination)
            if os.path.exists(source_filepath):
                print("Duplicating {} as {}".format(source_filepath, destination_filepath))
                copyfile(source_filepath, destination_filepath)
            else:
                print("File {} does not exist".format(source_filepath))

    def copy_files(self, source_path, output_path):
        for folder in self.config.FOLDERS_TO_CREATE:
            folder_fullpath = "{}{}".format(output_path, folder)
            if not os.path.exists(folder_fullpath):
                print("Creating folder {}".format(folder_fullpath))
                os.mkdir(folder_fullpath)

        for file in self.config.FILES_TO_COPY:
            source_filepath = "{}{}".format(source_path, file)
            destination_filepath = "{}{}".format(output_path, file)
            print("Copying {} into {}".format(source_filepath, destination_filepath))
            copyfile(source_filepath, destination_filepath)

    def remove_folders(self, output_path):
        for folder in self.config.FOLDERS_TO_REMOVE:
            folder_fullpath = "{}{}".format(output_path, folder)
            if os.path.exists(folder_fullpath):
                print("Removing folder {}".format(folder_fullpath))
                rmtree(folder_fullpath)

    def remove_files(self, output_path):
        for file in self.config.FILES_TO_REMOVE:
            file_fullpath = "{}{}".format(output_path, file)
            if os.path.exists(file_fullpath):
                print("Removing file {}".format(file_fullpath))
                os.remove(file_fullpath)
        if self.config.TRUNCATED_PAGINATION:
            self.truncate_pagination(output_path)

    def truncate_pagination(self, output_path):
        print("Truncating pagination files")
        for index in range(11, 900, 1):
            file_fullpath = "{}index{}.html".format(output_path, index)
            if os.path.exists(file_fullpath):
                os.remove(file_fullpath)
