"""

Idea of using BeautifulSoup from https://github.com/getpelican/pelican-plugins/blob/master/better_figures_and_images/

"""

import json
from io import BytesIO
import os
import tempfile

from bs4 import BeautifulSoup
from PIL import Image
import requests

from pelican import signals


class ImageCache():

    CACHE_FOLDER_NAME = "img_cache"
    CACHE_FILE_NAME = "cache.json"
    # TODO: Move to settings, but what default value to provide if not present?
    MAX_WIDTH = 748

    def __init__(self):
        self.cache = {}
        self.dirty = False

    def load(self, instance):
        cache_file = self._get_cache_file_path(instance)

        if os.path.exists(cache_file):
            with open(cache_file, "r") as file_handle:
                self.cache = json.load(file_handle)

    def save(self, instance):
        if not self.dirty:
            return

        cache_file = self._get_cache_file_path(instance)

        with open(cache_file, "w") as file_handle:
            json.dump(self.cache, file_handle)

    def get_image_width_and_height(self, image_path):
        if image_path in self.cache.keys():
            width, height = self.cache[image_path]
        else:
            print("Caching '{}'".format(image_path))
            request = requests.get(image_path)
            image = Image.open(BytesIO(request.content))
            width, height = image.size
            image.close()

            self.cache[image_path] = (width, height)
            self.dirty = True

        if width > self.MAX_WIDTH:
            # recalculate proportions and restrain image size
            original_proportion = width / height
            width = self.MAX_WIDTH
            height = int(width / original_proportion)

        return (width, height)

    @classmethod
    def _get_cache_file_path(cls, instance):
        base_path = os.path.dirname(instance.settings["PATH"])
        cache_path = os.path.join(base_path, cls.CACHE_FOLDER_NAME)

        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
            print("Created image cache folder '{}'".format(cache_path))

        return os.path.join(cache_path, cls.CACHE_FILE_NAME)


def content_object_init(instance):

    if instance._content is None:
        return

    image_cache = ImageCache()
    image_cache.load(instance)

    content = instance._content
    soup = BeautifulSoup(content, "html.parser")

    for img in soup(["img"]):
        # Text or similar containing a `<img>` tag
        if not img.get("src"):
            continue

        # Don't touch base64 encoded images
        img_path, _ = os.path.split(img["src"])
        if img_path.startswith("data:image"):
            continue

        # Always define width & height
        width, height = image_cache.get_image_width_and_height(img["src"])
        img["width"] = img.get("width", width)
        img["height"] = img.get("height", height)

        # Chrome's native lazy load
        img["loading"] = "lazy"

        # Good pratice
        if img.get("alt", "") == img["src"]:
            img["alt"] = ""

        # Old MCE cleanup
        if img.get("mce_src"):
            del img["mce_src"]

    image_cache.save(instance)

    instance._content = soup.decode()


def register():
    signals.content_object_init.connect(content_object_init)
