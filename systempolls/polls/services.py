from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist

from .models import Poll
from .serializers import PollSerializer, TextAnswerSerializer, ChoiceAnswerSerializer, MultiChoiceAnswerSerializer


def get_completed_polls(uid: int) -> list:
    result = []
    polls = Poll.objects.filter(user__id=uid)

    for poll in polls:
        serializer = PollSerializer(poll).data
        answers = []

        questions = poll.questions.all()
        for question in questions:

            if question.type == 'text':
                text_answer = question.text_answer
                text_answer_serializer = TextAnswerSerializer(text_answer).data
                answers.append(OrderedDict({'text_answer': text_answer_serializer}))

            if question.type == 'sc':
                try:
                    choice = question.selected_answer
                    choice_answer_serializer = ChoiceAnswerSerializer(choice).data

                except ObjectDoesNotExist:
                    choice_answer_serializer = []

                answers.append({'choice_answer': choice_answer_serializer})

            if question.type == 'mc':
                choices = question.selected_answers
                multi_choice_answer_serializer = MultiChoiceAnswerSerializer(choices, many=True).data
                answers.append({'multi_choice_answer': multi_choice_answer_serializer})

        serializer['questions'].append({'answers': answers})
        result.append(serializer)

    return result


def get_result_poll(uid) -> list:

    poll = Poll.objects

    if uid:
        result = get_completed_polls(uid)
    else:
        poll = poll.filter(is_active=True)
        result = PollSerializer(poll, many=True).data

    return result
