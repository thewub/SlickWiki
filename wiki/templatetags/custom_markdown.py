#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown
from markdown.extensions.toc import TocExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.wikilinks import WikiLinkExtension

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.text import slugify


def wikilink_url_builder(label, base, end):
    return '/' + slugify(label) + '/'



register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def custom_markdown(value):
    extensions = ['markdown.extensions.wikilinks', 
                  'markdown.extensions.footnotes',
                  TocExtension(baselevel=2, title='Contents', permalink=u'#'),
                  CodeHiliteExtension(guess_lang=True, use_pygments=True),
                  WikiLinkExtension(build_url=wikilink_url_builder)
                 ]
    return mark_safe(markdown.markdown(force_text(value),
                                        extensions,
                                        safe_mode=True,
                                        enable_attributes=False))