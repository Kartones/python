# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from shutil import copyfile


class AssetPostProcessor(object):

    # "aliases", in my case because of the old BlogEngine.NET feed
    FILES_TO_DUPLICATE = (
                          ('syndication.atom.xml', 'syndication.axd'),
                         )

    # Required for files to copy
    FOLDERS_TO_CREATE = (
                         'extra',
                        )

    # Because I don't want to have some stuff forcibly inside theme/...
    FILES_TO_COPY = (
                     'favicon.ico',
                     'robots.txt',
                     'extra/sample.file'
                    )

    # Because I already have bundles in a single css/js file
    FILES_TO_REMOVE = (
                       'theme/css/bootstrap.min.css',
                       'theme/css/font-awesome.min.css',
                       'theme/js/bootstrap.min.js',
                       'theme/js/jquery.min.js'
                      )

    def create_duplicates(self, output_path):
        for source, destination in self.FILES_TO_DUPLICATE:
            source_filepath = "{}{}".format(output_path, source)
            destination_filepath = "{}{}".format(output_path, destination)
            if os.path.exists(source_filepath):
                print("Duplicating {} as {}".format(source_filepath, destination_filepath))
                copyfile(source_filepath, destination_filepath)
            else:
                print("{} does not exist".format(source_filepath))

    def copy_files(self, source_path, output_path):
        for folder in self.FOLDERS_TO_CREATE:
            folder_fullpath = "{}{}".format(output_path, folder)
            if not os.path.exists(folder_fullpath):
                print("Creating folder {}".format(folder_fullpath))
                os.mkdir(folder_fullpath)

        for file in self.FILES_TO_COPY:
            source_filepath = "{}{}".format(source_path, file)
            destination_filepath = "{}{}".format(output_path, file)
            print("Copying {} into {}".format(source_filepath, destination_filepath))
            copyfile(source_filepath, destination_filepath)

    def remove_files(self, output_path):
        for file in self.FILES_TO_REMOVE:
            file_fullpath = "{}{}".format(output_path, file)
            if os.path.exists(file_fullpath):
                print("Removing file {}".format(file_fullpath))
                os.remove(file_fullpath)

if __name__ == '__main__':
    output_path = "./output/"
    post_processor = AssetPostProcessor()
    post_processor.create_duplicates(output_path)
    post_processor.copy_files("./themes/kartones-blog/extra-files/", output_path)
    post_processor.remove_files(output_path)
