from questionnaire import *
from django.utils.translation import ugettext as _, ungettext
from json import dumps
from questionnaire.utils import get_answer, get_answer_multiple, parse_int

def get_freeform_position(question):
    cd = question.getcheckdict()
    freeform_position = cd.get('freeform_position')

    if freeform_position:
        return int(freeform_position)
    else:
        return None

@question_proc('choice', 'select')
def question_choice(request, question):
    choices = []
    jstriggers = []
    cd = question.getcheckdict()
    freeform_position = get_freeform_position(question)

    val = None
    comment = ''
    remark = ''
    answer = get_answer(question, request, True)
    if answer:
        val = answer[0]
        if len(answer) == 2:
            if freeform_position:
                comment = answer[1]
            else:
                remark = answer[1]
        elif len(answer) == 3:
            comment = answer[1]
            remark = answer[2]
    elif 'default' in cd:
        val = cd['default']

    for choice in question.choices():
        choices.append( ( choice.value == val, choice, ) )

    if freeform_position:
        jstriggers.append('%s_comment' % question.number)

    return {
        'freeform_text': cd.get('freeform_text', ''),
        'freeform_position': freeform_position,
        'choices'   : choices,
        'qvalue'    : val or '',
        'required'  : True,
        'comment'   : comment,
        'jstriggers': jstriggers,
        'remarks': cd.get('remarks', None),
        'remark_value': remark
    }

@answer_proc('choice', 'select')
def process_choice(question, answer):
    opt = answer['ANSWER'] or ''
    freeform_position = get_freeform_position(question)
    freeform_choice_value = question.choices()[freeform_position-1].value if freeform_position else None
    comment = None
    remarks = answer.get('remarks', None)

    if not opt:
        raise AnswerException(_(u'You must select an option'))
    if opt == freeform_choice_value:
        comment = answer.get('comment','')
        if not comment:
            raise AnswerException(_(u'Field cannot be blank'))
    else:
        valid = [c.value for c in question.choices()]
        if opt not in valid:
            raise AnswerException(_(u'Invalid option!'))

    result = [ v for v in [opt, comment, remarks] if v ] # only not-None values
    return dumps(result)
add_type('choice', 'Choice [radio]')

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
