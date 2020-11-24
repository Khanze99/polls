from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist

from .models import Poll, CompletedPoll
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
