from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist

from .models import Poll
from .serializers import PollSerializer


def get_completed_polls(uid: int) -> list:
    """ Получаем пройденные опросы """
    result = []

    return result


def get_result_poll(uid) -> list:

    if uid:
        result = get_completed_polls(uid)
    else:
        result = PollSerializer(Poll.objects.filter(is_active=True), many=True).data

    return result
