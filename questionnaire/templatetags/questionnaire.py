#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from ..utils import has_tag
import re
from fileinput import close

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

@register.filter(name='adapt')
def adapt(text, runinfo): 
    """Adapts the text to the sex and age of the subject
    Converts string in a form:
    'xxx { [formal_male/formal_female]/[informal_male/informal_female]} xxx'
    to e.g. 'xxx formal_female xxx' if the person is a femal of age.
    """

    if not text:
        return None
    
    text = _adapt(text, runinfo, '[', ']', 'male', 'female')
    text = _adapt(text, runinfo, '{', '}', 'of_age', None, 1)

    return text

def _adapt(text, runinfo, opening_tag, closing_tag, option1_tag, option2_tag, default=None):
    regex = '\%s[^\]]*\%s' % (opening_tag, closing_tag)
    expressions = re.findall(regex, text)

    for expression in expressions:
        is_option1 = has_tag(option1_tag, runinfo)
        is_option2 = has_tag(option2_tag, runinfo)
 
        correct_form = expression.strip(opening_tag+closing_tag)

        form_choices = correct_form.split('/')
        if is_option1 or is_option2:
            correct_form = form_choices[is_option2]
        elif default:
            correct_form = form_choices[default]

        text = text.replace(expression, correct_form)

    return text
