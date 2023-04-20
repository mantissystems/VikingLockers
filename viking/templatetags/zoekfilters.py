from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaksbr, urlize
from re import IGNORECASE, compile, escape as rescape

register = template.Library()
@register.filter
def highlight(text, search):
    rgx = compile(rescape(search), IGNORECASE)
    return mark_safe(
        rgx.sub(
            lambda m: '<b class="text text-danger">{}</b>'.format(m.group()),
            text
        )
    )
# register.filter("highlight", highlight)

# @register.filter
# def bevat(text, search):
#     rgx = compile(rescape(search), IGNORECASE)
#     return mark_safe(
#         rgx.sub(
#             lambda m: '<b class="text text-danger">{}</b>'.format(m.group()),
#             text
#         )
#     )
# @register.filter(needs_autoescape=True)
# def initial_letter_filter(text, autoescape=True):
#     first, other = text[0], text[1:]
#     if autoescape:
#         esc = conditional_escape
#     else:
#         esc = lambda x: x
#     result = '<strong>%s</strong>%s' % (esc(first), esc(other))
#     return mark_safe(result)
