from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from .models import Poll, CompletedPoll, Choice, Question
from .serializers import PollSerializer, CompletedPollSerializer, QuestionSerializer


def get_completed_polls(uid):
    """ Получаем пройденные опросы """
    polls_ids = CompletedPoll.objects.distinct('poll_id').filter(user__id=uid).values_list('poll_id')
    result = []
    for poll_id in polls_ids:
        # completed_polls = CompletedPoll.objects.select_related('poll', 'user', 'question', 'choice').filter(poll_id=poll_id)
        completed_polls = CompletedPoll.objects.filter(poll_id=poll_id)
        completed_polls_serializer = CompletedPollSerializer(completed_polls, many=True)
        result.append(completed_polls_serializer.data)

    return result


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
