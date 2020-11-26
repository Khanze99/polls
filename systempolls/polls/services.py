from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from .models import Poll, CompletedPoll, Choice, Question
from .serializers import PollSerializer, CompletedPollSerializer


def get_completed_polls(uid):
    """ Получаем пройденные опросы """
    serializer = CompletedPollSerializer(CompletedPoll.objects.filter(user__id=uid), many=True).data

    return serializer


def get_result_poll(uid):

    if uid:
        result = get_completed_polls(uid)
    else:
        result = PollSerializer(Poll.objects.filter(is_active=True), many=True).data

    return result


def save_results(data):
    completed_polls = []
    questions = data['questions']

    try:
        poll = Poll.objects.get(id=data['poll_id'])
    except ObjectDoesNotExist:
        return False, 'poll_id: {}'.format(data['poll_id'])

    try:
        user = User.objects.get(id=data['uid'])
    except ObjectDoesNotExist:
        user = None

    for question in questions:
        try:
            q = Question.objects.get(id=question['question_id'])
        except ObjectDoesNotExist:
            return False, 'question_id: {}'.format(question['question_id'])

        type_question = question['type']
        answer = question['answer']

        if type_question == 'text':
            completed_polls.append(CompletedPoll(user=user, poll=poll, question=q, text=answer))

        if type_question == 'sc':
            try:
                choice = Choice.objects.get(id=answer)
            except ObjectDoesNotExist:
                return False, 'choice_id: {}'.format(answer)

            completed_polls.append(CompletedPoll(user=user, poll=poll, question=q, choice=choice))

        if type_question == 'mc':
            choices = Choice.objects.filter(id__in=answer)
            for choice in choices:
                completed_polls.append(CompletedPoll(user=user, poll=poll, question=q, choice=choice))

    CompletedPoll.objects.bulk_create(completed_polls)

    return True, None
