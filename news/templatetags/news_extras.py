import re

from django import template

register = template.Library()

# Match any character in the main Arabic Unicode blocks (covers Arabic,
# Arabic Supplement, Arabic Extended-A, and the Presentation Forms A/B).
_ARABIC_RE = re.compile(
    r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]"
)


@register.filter(name="arabic_class")
def arabic_class(value):
    """Return 'lang-ar' if the string contains Arabic characters, else ''.

    Use to flip an element to the Alyamama font + RTL direction:
        <h1 class="{{ news.name|arabic_class }}">{{ news.name }}</h1>
    """
    if value and _ARABIC_RE.search(str(value)):
        return "lang-ar"
    return ""
