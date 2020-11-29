from django.contrib.auth.models import User

from .models import Poll, CompletedPoll, Choice, Question
from .serializers import PollSerializer, GetCompletedPollSerializer, QuestionSerializer, PostCompletedPollSerializer


def get_completed_polls(uid):
    """ Получаем пройденные опросы """

    completed_polls = CompletedPoll.objects.filter(user__id=uid)
    result = GetCompletedPollSerializer(completed_polls, many=True).data

    return result


def get_result_poll(uid):
    if uid:
        result = get_completed_polls(uid)

    else:
        result = PollSerializer(Poll.objects.filter(is_active=True), many=True).data

    return result


def save_results(data):

    serializer = PostCompletedPollSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.create(data)

