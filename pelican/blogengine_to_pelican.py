#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import re

# TODO: Handle nasty windows characters inserted like the following, which cause encoding errors (fixed now by manual replacing at source xmls)
# ’  -> '
# “ -> "
# ” -> "
# … -> ...

class BlogEngineToPelican(object):
  """
  Script to migrate posts from BlogEngine.net to Pelican.
  Read http://blog.kartones.net/post/migrating-from-blogengine-to-pelican for more info.
  """

    # From categories.xml
    CATEGORIES = {
                  "5a298087-8776-44b8-b9b9-bf2ba5331b19": "App Reviews",
                  "f58b6ec4-6784-43e4-bfdd-56313c0984d7": "Architecture",
                  "7ee3808f-2901-44da-9856-ccccb82d11a1": "Book Reviews",
                  "4965826d-06cf-4cee-aab2-81f285cd8ee1": "Databases",
                  "82b34667-a2e4-44ba-9766-667f31894ba8": "Development",
                  "43c00226-122f-4234-bde3-f8d690f86faf": "Game Dev",
                  "17e89720-22ab-4cdc-be54-e7774aeb89db": "Gaming",
                  "e132c2a6-866b-451d-9516-8f5ae856a46e": "Graphics",
                  "0116880a-ac0f-4a59-85aa-dd553608668c": "Kartones.Net",
                  "63b42e46-473d-4d14-be0b-2ac052bc604f": "Mobile Dev",
                  "0f1704b8-18ac-47bc-9fd8-158be9ebe220": "Offtopic",
                  "6a731ee0-61a8-48bd-ab36-2a04261d793e": "Security",
                  "113570c5-3768-4007-b972-a3784a6ef45c": "Social",
                  "b8b4629e-f6c7-4403-a7a6-4d2f255dbb7c": "Systems-IT",
                  "ceb079b1-ded8-4c5d-8063-76ea80da3f30": "Testing",
                  "195cddac-fc59-4745-9b26-ec680696196b": "Tools",
                  "fd5105d2-810b-41a5-83ee-f5d0dded471f": "UX",
                  "41a19c55-05af-43f6-a2be-23f1b2c3a749": "Virtualization"
                 }

    REPLACEMENTS = (
                    ("&amp;amp;", "&amp;"),
                    ("&amp;nbsp;", " "),
                    ("&lt;", "<"),
                    ("&gt;", ">")
                   )


    def work(self, path):
        files = os.listdir(path)
        for filename in files:
            file_fullpath = "{}{}".format(path, filename)
            file_data = self._read_file(file_fullpath)
            post_datetime = self._get_post_datetime(file_data)
            destination_file_fullpath = self._rename_file(path, file_fullpath, post_datetime.split(" ")[0])
            if destination_file_fullpath is None:
                print("ERROR: ", end="")
            else:
                title = self._get_post_title(file_data)
                slug = self._get_post_slug(file_data)
                datetime = self._get_post_datetime(file_data)
                tags = self._get_post_tags(file_data)
                contents = self._get_post_contents(file_data)

                file_data = self._get_output_content(title, slug, datetime, tags, contents)
                self._write_file(destination_file_fullpath, file_data)
            print(filename)


    def _perform_replacements(self, file_data):
        for (search, replace) in self.REPLACEMENTS:
            file_data = file_data.replace(search, replace)
        return file_data


    def _get_output_content(self, title, slug, datetime, tags, content):
        return "Title: {}\nSlug: {}\nDate: {}\nTags: {}\n\n {}".format(title, slug, datetime, ",".join(tags), content)

    def _get_post_contents(self, file_data):
        matches = re.match( r'.*<content>(.*)</content>.*', file_data, re.I | re.S)
        contents = matches.group(1)
        return self._perform_replacements(contents)


    # Tags never worked too well at BlogEngine, so I used Categories in their instead
    def _get_post_tags(self, file_data):
        matches = re.match( r'.*<category>(.*)</category>.*', file_data, re.I | re.S)
        return [self.CATEGORIES[group] for group in matches.groups()]


    def _get_post_title(self, file_data):
        matches = re.match( r'.*<title>(.*)</title>.*', file_data, re.I | re.S)
        return matches.group(1)


    def _get_post_slug(self, file_data):
        matches = re.match( r'.*<slug>(.*)</slug>.*', file_data, re.I | re.S)
        return matches.group(1)


    def _get_post_datetime(self, file_data):
        matches = re.match( r'.*<pubdate>(.*)</pubdate>.*', file_data, re.I | re.S)
        return matches.group(1)


    def _read_file(self, file_fullpath):
        file_handle = open(file_fullpath, "r", errors="ignore")
        file_data = file_handle.read()
        file_handle.close()
        return file_data


    def _write_file(self, file_fullpath, contents):
        file_handle = open(file_fullpath, "w")
        file_handle.write(contents)
        file_handle.close()


    # Instead of checking if file exists, just rename as will get replaced
    def _rename_file(self, path, source_file_fullpath, article_date, retried_count=0):
        if retried_count > 0:
            # YYYY-MM-DD-2 onwards
            destination_name = "{}-{}.md".format(article_date, retried_count+1)
        else:
            destination_name = "{}.md".format(article_date)
        destination_file_fullpath = "{}{}".format(path, destination_name)
        try:
            os.rename(source_file_fullpath, destination_file_fullpath)
        except OSError as os_exception:
            if retried_count < 9:
                return self._rename_file(path, source_file_fullpath, article_date, retried_count+1)
            else:
                print("Error renaming {} to {}: {}".format(source_file_fullpath, destination_file_fullpath,
                                                           os_exception))
                return None
        return destination_file_fullpath


if __name__ == '__main__':
    migrator = BlogEngineToPelican()
    # Must have trailing slash
    migrator.work("./old_content/posts/")
