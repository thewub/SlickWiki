#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown, bleach

from markdown.extensions.toc import TocExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.wikilinks import WikiLinkExtension

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.text import slugify


# Tags suitable for rendering markdown (based on https://github.com/yourcelf/bleach-whitelist)
markdown_tags = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "b", "i", "strong", "em", "tt",
    "p", "br",
    "span", "div", "blockquote", "code", "hr",
    "ul", "ol", "li", "dd", "dt",
    "img",
    "a",
    "pre",
    "sup"
]

markdown_attrs = {
    "*": ["class", "id"],
    "img": ["src", "alt", "title"],
    "a": ["href", "alt", "title", "class", "id"]
}

def wikilink_url_builder(label, base, end):
    return '/' + slugify(label) + '/'


register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def custom_markdown(value):
    extensions = ['markdown.extensions.wikilinks', 
                  'markdown.extensions.footnotes',
                  TocExtension(baselevel=2, title='Contents', permalink=u'#', marker='{-TOC-}'),
                  CodeHiliteExtension(guess_lang=True, use_pygments=True),
                  WikiLinkExtension(build_url=wikilink_url_builder)
                 ]
    return mark_safe(
        bleach.clean(
            markdown.markdown(force_text(value), extensions=extensions),
            markdown_tags, 
            markdown_attrs
            )
        )

# Hack to always add a TOC
@register.filter(is_safe=True)
@stringfilter
def add_toc(value):
    return mark_safe( '{-TOC-}\n\n' + value )
