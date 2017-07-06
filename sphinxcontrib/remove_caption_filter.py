# -*- coding: utf-8 -*-
"""
remove caption filter
---------------------

This is a filter of pandoc.

Mark down Image:

    [alt](path)

Convert as below:

    [](path alt)

"""
import os
from pandocfilters import toJSONFilter, Image, Link, RawInline
import logging

try:
    import urlparse
except ImportError:
    from urllib.parse import urlparse

log = logging.getLogger(os.path.basename(__file__))


def configure_logging(f):
    format_string = "%(name)s: [%(levelname)s] %(message)s"
    logging.basicConfig(format=format_string, level=logging.DEBUG)
    log.debug("Debug logging enabled.")

    return f


def remove_caption_filter(key, value, format_, meta):
    if key == 'Image':
        """
        markdown:
            ![alt](path "title")

        json:
            [[u'', [], []], [{u'c': u'alt', u't': u'Str'}], [u'path', u'fig:title']]
        """
        try:
            alt = value[1][0].get("c")
        except IndexError:
            alt = None

        value[1] = []

        if alt:
            value[2][1] = u"fig:{}".format(alt)
        return Image(*value)
    elif key == "Link":
        """
        markdown:
            [node](node_api.md)
            [](README.md)
        json:
            [[u'', [], []], [{u'c': u'node', u't': u'Str'}], [u'node_api.md', u'']]
            [[u'', [], []], [], [u'README.md', u'']]
        """
        link_path = value[2][0]
        if not bool(urlparse.urlparse(link_path).netloc):
            name, ext = os.path.splitext(link_path)
            if ext and ext.lower() == ".md":

                log.info('value: {}'.format(value))
                if value[1]:
                    link_name = value[1][0]["c"]
                else:
                    link_name = None

                if link_name:
                    return RawInline(u'rst', u':doc:`{} <{}>`'.format(link_name, name))
                return RawInline(u'rst', u':doc:`{}`'.format(name))

        return Link(*value)


if __name__ == "__main__":
    toJSONFilter(configure_logging(remove_caption_filter))
