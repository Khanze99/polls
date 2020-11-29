from .models import Poll, CompletedPoll
from .serializers import PollSerializer, GetPollSerializer, PostCompletedPollSerializer


def get_completed_polls(uid):
    """ Получаем пройденные опросы """

    completed_polls = CompletedPoll.objects.filter(user__id=uid).distinct('poll_id')
    poll_ids = [cp.poll_id for cp in completed_polls]
    polls = Poll.objects.filter(id__in=poll_ids)
    result = GetPollSerializer(polls, many=True).data

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

