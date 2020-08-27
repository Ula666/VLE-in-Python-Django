# topic_quiz.py
from django.db import transaction
from .models import Response


# Every question is an object called - QuizQuestion
def render_quiz(questions, data=None):
    if data is None:
        data = {}

    html = ''

    i = 0
    for question in questions:
        html += '<p>' + question.text + '</p>'
        html += '\n'

        question_name = "question_" + str(i)
        value = data.get(question_name)

        html += '<select name="' + question_name + '">'

        if value:
            html += '<option disabled value> -- select an option -- </option>'
        else:
            html += '<option disabled selected value> -- select an option -- </option>'

        if value == question.answer_4:
            html += '<option value="answer_1" selected >' + question.answer_1 + '</option>'
        else:
            html += '<option value="answer_1">' + question.answer_1 + '</option>'

        html += '\n'

        if value == question.answer_4:
            html += '<option value="answer_2" selected >' + question.answer_2 + '</option>'
        else:
            html += '<option value="answer_2">' + question.answer_2 + '</option>'

        html += '\n'

        if value == question.answer_4:
            html += '<option value="answer_3" selected >' + question.answer_3 + '</option>'
        else:
            html += '<option value="answer_3">' + question.answer_3 + '</option>'

        html += '\n'

        if value == question.answer_4:
            html += '<option value="answer_4" selected >' + question.answer_4 + '</option>'
        else:
            html += '<option value="answer_4">' + question.answer_4 + '</option>'

        html += '\n'

        html += '</select>'
        html += '\n'
        i += 1
    return html


def is_valid(questions, data):
    for nr in range(len(questions)):
        name = "question_" + str(nr)
        value = data.get(name)
        if not value:
            return False
    return True


def save_quiz_responses(questions, data, user):
    with transaction.atomic():
        nr = 0
        for question in questions:
            name = "question_" + str(nr)
            answer = data.get(name)
            response = Response(
                quizquestion=question,
                quizanswer=answer,
                user=user
            )
            response.save()
            nr += 1
