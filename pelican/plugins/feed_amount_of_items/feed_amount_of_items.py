# -*- coding: utf-8 -*-
"""
Feed Amount of Items
====================

This plugin allows to reduce feed to a certain amount of items instead of the whole contents.
Heavily based on https://github.com/getpelican/pelican-plugins/tree/master/feed_summary
"""
from __future__ import unicode_literals
from jinja2 import Markup

import six
if not six.PY3:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from pelican import signals
from pelican.writers import Writer
from pelican.utils import set_date_tzinfo

from .magic_set import magic_set

class LimitedFeedWriter(Writer):

    def _add_item_to_the_feed(self, feed, item):
        if not hasattr(self, 'amounts'):
            self.amounts = {}

        if self.settings['FEED_AMOUNT_OF_ITEMS'] > 0:
            feed_name = feed.__class__.__name__
            if self.amounts.get(feed_name, None) is None:
                self.amounts[feed_name] = 0
            if self.amounts[feed_name] < self.settings['FEED_AMOUNT_OF_ITEMS']:
                self.amounts[feed_name] = self.amounts[feed_name] + 1
                super(LimitedFeedWriter, self)._add_item_to_the_feed(feed, item)
        else:
            super(LimitedFeedWriter, self)._add_item_to_the_feed(feed, item)

def set_plugin_default_settings(pelican_object):
    pelican_object.settings.setdefault('FEED_AMOUNT_OF_ITEMS', 25)

def patch_pelican_writer(pelican_object):
    @magic_set(pelican_object)
    def get_writer(self):
        return LimitedFeedWriter(self.output_path, settings=self.settings)

def register():
    signals.initialized.connect(set_plugin_default_settings)
    signals.initialized.connect(patch_pelican_writer)