# -*- coding: utf-8 -*-
"""

Writes a `.md` sidecar next to every generated output file: a copy of the original Markdown source for articles/pages,
and a generated links listing for tag/category/author/archives/index pages. Also populates a llms.txt file,
based on a template.

Implements https://llmstxt.org/

Settings (see pelicanconf.py):
    LLMS_EXPORT_CONTENT_EXCLUSIONS: slugs to skip when exporting individual article/page sources.
    LLMS_EXPORT_LISTING_EXCLUSIONS: page_name values to skip when exporting listing pages.
    LLMS_EXPORT_MAX_INDEX_PAGES: how many paginated index.html pages to export.

"""

from __future__ import unicode_literals

import os
import shutil
from logging import warning

from pelican import signals


def _write_content_source(destination, content_object, context):
    exclusions = context.get("LLMS_EXPORT_CONTENT_EXCLUSIONS", [])
    if getattr(content_object, "slug", None) in exclusions:
        return

    source_path = getattr(content_object, "source_path", None)
    if not source_path or not os.path.isfile(source_path):
        warning("llms_export plugin: source file not found for {}".format(destination))
        return

    shutil.copyfile(source_path, destination)


def _listing_title(context):
    if "tag" in context:
        return "Tag: {}".format(context["tag"].name)
    if "category" in context:
        return "Category: {}".format(context["category"].name)
    if "author" in context:
        return "Author: {}".format(context["author"].name)
    if "period" in context:
        return "Archive: {}".format(" ".join(str(p) for p in context["period"]))

    page_name = context.get("page_name")
    if page_name == "index":
        page = context.get("articles_page")
        if page is not None:
            return "{} - page {}".format(page_name, page.number)
    return page_name


def _listing_articles(context):
    page = context.get("articles_page")
    if page is not None:
        return page.object_list
    return context.get("articles") or []


def _article_line(article, siteurl):
    url = "{}/{}".format(siteurl, article.url) if siteurl else "/" + article.url
    return "- [{}]({}) - {}".format(article.title, url, article.date.strftime("%Y-%m-%d"))


def _write_tags_source(destination, context):
    tags = context.get("tags") or []
    if not tags:
        return

    siteurl = context.get("SITEURL", "")
    lines = ["# Tags", ""]
    for tag, articles in sorted(tags, key=lambda entry: entry[0].name.lower()):
        lines.append("## {}".format(tag.name))
        lines.append("")
        for article in articles:
            lines.append(_article_line(article, siteurl))
        lines.append("")

    with open(destination, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")


def _write_listing_source(destination, context):
    filename = context.get("page_name")
    listing_exclusions = context.get("LLMS_EXPORT_LISTING_EXCLUSIONS", [])
    if filename in listing_exclusions:
        return

    if filename == "tags":
        _write_tags_source(destination, context)
        return

    if filename == "index":
        page = context.get("articles_page")
        max_index_pages = context.get("LLMS_EXPORT_MAX_INDEX_PAGES", 9)
        if page is not None and page.number > max_index_pages:
            return

    articles = _listing_articles(context)
    if not articles:
        return

    siteurl = context.get("SITEURL", "")
    lines = ["# {}".format(_listing_title(context)), ""]
    for article in articles:
        lines.append(_article_line(article, siteurl))

    with open(destination, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def export_markdown_source(path, context):
    destination = path + ".md"

    content_object = context.get("article") or context.get("page")
    if content_object is not None:
        _write_content_source(destination, content_object, context)
        return

    # page_name/period are only set by Pelican for listing-style writes (tag,
    # category, author, archives, index, ...), never for individual
    # article/page writes, so together they reliably tell the two cases apart.
    # (template_name looks like the natural marker, but Writer.write_file()
    # consumes it as a named parameter and never forwards it into context.)
    if "page_name" in context or "period" in context:
        _write_listing_source(destination, context)


def register():
    signals.content_written.connect(export_markdown_source)
