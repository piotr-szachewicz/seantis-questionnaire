#!/usr/bin/python

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from ..utils import has_tag
import re

register = template.Library()


@register.filter(name="dictget")
def dictget(thedict, key):
    "{{ dictionary|dictget:variableholdingkey }}"
    return thedict.get(key, None)


@register.filter(name="spanclass")
def spanclass(string):
    l = 2 + len(string.strip()) // 6
    if l <= 4:
        return "span-4"
    if l <= 7:
        return "span-7"
    if l < 10:
        return "span-10"
    return "span-%d" % l

@register.filter(name="qtesturl")
def qtesturl(question):
    qset = question.questionset
    return reverse("questionset",
        args=("test:%s" % qset.questionnaire().id,
         qset.sortid))

@register.filter(name='adapt_to_sex')
def adapt_to_sex(text, runinfo): # Only one argument.
    """Adapts the text to the """
    expressions = re.findall('\[[^\]]*\]', text)
    for expression in expressions:
        is_male = has_tag('male', runinfo)
        is_female = has_tag('female', runinfo)

        correct_form = expression.strip('[]')
        if is_male or is_female:
            correct_form = correct_form.split('/')[is_female]

        text = text.replace(expression, correct_form)
    return text
