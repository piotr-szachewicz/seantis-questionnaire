from questionnaire import *
from django.utils.translation import ugettext as _, ungettext
from json import dumps
from questionnaire.utils import get_answer, get_answer_multiple, parse_int

@question_proc('choice', 'choice-freeform', 'select')
def question_choice(request, question):
    choices = []
    jstriggers = []
    cd = question.getcheckdict()

    val = None
    comment = ''
    answer = get_answer(question, request, True)
    if answer:
        val = answer[0]
        if len(answer) == 2:
            comment = answer[1]
    elif 'default' in cd:
        val = cd['default']

    for choice in question.choices():
        choices.append( ( choice.value == val, choice, ) )

    if question.type == 'choice-freeform':
        jstriggers.append('%s_comment' % question.number)

    return {
        'freeform_text': cd.get('freeform_text', ''),
        'choices'   : choices,
        'sel_entry' : val == '_entry_',
        'qvalue'    : val or '',
        'required'  : True,
        'comment'   : comment,
        'jstriggers': jstriggers,
    }

@answer_proc('choice', 'choice-freeform', 'select')
def process_choice(question, answer):
    opt = answer['ANSWER'] or ''
    if not opt:
        raise AnswerException(_(u'You must select an option'))
    if opt == '_entry_' and question.type == 'choice-freeform':
        comment = answer.get('comment','')
        if not comment:
            raise AnswerException(_(u'Field cannot be blank'))
        return dumps([opt, comment])
    else:
        valid = [c.value for c in question.choices()]
        if opt not in valid:
            raise AnswerException(_(u'Invalid option!'))
    return dumps([opt])
add_type('choice', 'Choice [radio]')
add_type('choice-freeform', 'Choice with a freeform option [radio]')


@question_proc('choice-multiple', 'choice-multiple-freeform')
def question_multiple(request, question):
    cd = question.getcheckdict()
    [choices, extras, jstriggers] = get_answer_multiple(question, request)

    return {
        "choices": choices,
        "extras": extras,
        "template"  : "questionnaire/choice-multiple-freeform.html",
        "required" : cd.get("required", False) and cd.get("required") != "0",
        'jstriggers': jstriggers,
    }

@answer_proc('choice-multiple', 'choice-multiple-freeform')
def process_multiple(question, answer):
    multiple = []
    multiple_freeform = []
    clarify = {}
    choices_count = question.choices().count()

    required = question.getcheckdict().get('required', 0)
    requiredcount = 0
    if required:
        requiredcount = parse_int(required, 1)
    if requiredcount and requiredcount > choices_count:
        requiredcount = question.choices().count()

    maxcount = question.getcheckdict().get('maxcount', None)    
    maxcount = parse_int(maxcount, None)

    for k, v in answer.items():
        if k.startswith('multiple'):
            multiple.append(v)
        if k.startswith('more'):
            multiple_freeform.append(v)
        if k.startswith('clarify'):
            clarify[k.replace('clarify_', '')] = v
            if len(v.strip()) == 0:
                raise AnswerException(_(u'Field cannot be blank'))

    number_of_choices = len(multiple) + len(multiple_freeform)
    if number_of_choices < requiredcount:
        raise AnswerException(ungettext(u"You must select at least %d option",
                                        u"You must select at least %d options",
                                        requiredcount) % requiredcount)
    if maxcount and number_of_choices > maxcount:
        raise AnswerException(ungettext(u"You can select at most %d option",
                                        u"You can select at most %d options",
                                        maxcount) % maxcount)

    multiple.sort()
    multiple.append(clarify)
    if multiple_freeform:
        multiple.append(multiple_freeform)
    return dumps(multiple)

add_type('select', 'Drop-down list [select]')
add_type('choice-multiple', 'Multiple-Choice, Multiple-Answers [checkbox]')
add_type('choice-multiple-freeform', 'Multiple-Choice, Multiple-Answers, plus freeform [checkbox, input]')
