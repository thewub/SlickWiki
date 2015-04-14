#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown
from markdown.extensions.toc import TocExtension
from markdown.extensions.codehilite import CodeHiliteExtension

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def custom_markdown(value):
    extensions = ['wikilinks', 
                  TocExtension(baselevel=2, title='Contents', permalink=u'#'),
                  CodeHiliteExtension(guess_lang=True, use_pygments=True)]
    return mark_safe(markdown.markdown(force_unicode(value),
                                        extensions,
                                        safe_mode=True,
                                        enable_attributes=False))