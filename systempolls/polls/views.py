from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll
from .serializers import PollSerializer


class PollView(APIView):
    """Получение активных опросов, пройденных опросов по ID, прохождение опросов по ID"""

    def get(self, request, uid=None):
        poll = Poll.objects
        print(uid)

        if uid:
            # логика: получение опросов по id + ответы
            poll = poll.filter(user__id=uid)
            serializer = {}
        else:
            poll = poll.filter(is_active=True)
            serializer = PollSerializer(poll, many=True).data

        return Response(serializer)

    def post(self, request):
        ...
