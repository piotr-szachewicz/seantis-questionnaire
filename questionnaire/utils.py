#!/usr/bin/python
from django.conf import settings
from json import loads

def split_numal(val):
    """Split, for example, '1a' into (1, 'a')
>>> split_numal("11a")
(11, 'a')
>>> split_numal("99")
(99, '')
>>> split_numal("a")
(0, 'a')
>>> split_numal("")
(0, '')
    """
    if not val:
        return 0, ''
    for i in range(len(val)):
        if not val[i].isdigit():
            return int(val[0:i] or '0'), val[i:]
    return int(val), ''
        

def numal_sort(a, b):
    """Sort a list numeric-alphabetically

>>> vals = "1a 1 10 10a 10b 11 2 2a z".split(" "); \\
... vals.sort(numal_sort); \\
... " ".join(vals)
'z 1 1a 2 2a 10 10a 10b 11'
    """
    anum, astr = split_numal(a)
    bnum, bstr = split_numal(b)
    cmpnum = cmp(anum, bnum)
    if(cmpnum == 0):
        return cmp(astr, bstr)
    return cmpnum

def numal0_sort(a, b):
    """
    numal_sort on the first items in the list
    """
    return numal_sort(a[0], b[0])

def has_tag(tag, runinfo):
    """ Returns true if the given runinfo contains the given tag. """
    return tag in (t.strip() for t in runinfo.tags.split(','))

def get_answer(question, request, multiple=False):
    from models import Answer
    # get current question value - from request or from the database
    current = None
    if request:
        current = request.POST.get('question_%s' % question.number, None)
    if not current:
        # if the current value doesn't exist in the POST data, find one in the database 
        answer = Answer.get_answer(request.runinfo.runid, question.id)
        if answer:
            current = answer.split_answer()
            if current and not multiple:
                return current[0]
    return current

def get_answer_multiple(question,request):    
    cd = question.getcheckdict()
    defaults = cd.get('default','').split(',')
    extracount = int(cd.get('extracount', 0))
    if not extracount and question.type == 'choice-multiple-freeform':
        extracount = 1
    clarify_choices = loads(cd.get('clarify_choices', '{}').replace('\'', '\"'))

    choices = []
    extra_answers = []
    clarify_answers = {}
    answers = get_answer(question, request, True)
    if answers:
        if extracount > 0:
            extra_answers = answers[-1]
        if clarify_choices:
            try:
                clarify_answers = answers[-(extracount>0)-1]
                if type(clarify_answers) is not dict:
                    clarify_answers = {}
            except IndexError:
                clarify_answers = {}
    else:
        answers = []      

    jstriggers = []

    for idx, choice in enumerate(question.choices()):
        key = "question_%s_multiple_%d" % (question.number, choice.sortid)
        checked = ''

        if key in request.POST or choice.value in answers or \
            (request.method == 'GET' and choice.value in defaults):
            checked = ' checked'

        clarify_text = clarify_choices.get(choice.value, None)
        if clarify_text:
            clarify_key = "question_%s_clarify_%s" % (question.number, choice.value)
            clarify = {'text': clarify_text, 'key': clarify_key, 'value': clarify_answers.get(choice.value, '')}
            jstriggers.append(clarify_key)
        else:
            clarify = None

        choices.append( (choice, key, checked,  clarify) )

    extras = []
    for i in range(extracount):
        key = "question_%s_more_%d" % (question.number, i+1)

        data = ''
        if key in request.POST:
            data = request.POST[key]
        elif len(extra_answers) > i:
            data = extra_answers[i]

        extras.append( (key, data,) )

    return choices, extras, jstriggers

def get_setting(key, default=None):
    try:
        return getattr(settings, key, default) 
    except AttributeError:
        return default

def parse_int(str, default=None):
    if str:
        try:
            return int(str)
        except ValueError:
            return default
    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
