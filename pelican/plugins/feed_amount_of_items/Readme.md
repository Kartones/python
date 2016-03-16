# Feed Amount of Items
This plugin allows to reduce feed to a certain amount of items instead of the whole contents.

Via a setting variable, you can ontrol how many items are written in the Atom and RSS feeds output, because for big blogs with hundreds of articles those files easily get above 1MB in size and it is common practice to just output the last N items to keep the responses small.

## Usage
To use this plugin, ensure the following are set in your `pelicanconf.py` file:

    PLUGIN_PATH = '/path/to/pelican-plugins'
    PLUGINS = [
		'plugins.feed_amount_of_items',
		]
    FEED_AMOUNT_OF_ITEMS = 25

The default value of `FEED_AMOUNT_OF_ITEMS` is `25` (enabled). Any value greater than zero acts as the limit, `0` or less means `disabled`.

This plugin has been tested with pelican 3.6 onwards.

## Notes

Heavily based on [feed summary plugin](https://github.com/getpelican/pelican-plugins/tree/master/feed_summary).

It probably cuts also author and tag feeds. It's been only tested (and intended for) using with `FEED_ATOM` and `FEED_RSS`.