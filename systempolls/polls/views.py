from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import Poll
from .serializers import PollSerializer


class PollView(APIView):
    """Получение активных опросов, пройденных опросов по ID, прохождение опросов по ID"""

    def get(self, request, uid=None):
        poll = Poll.objects

        if uid:
            # логика: получение опросов по id + ответы
            polls = poll.filter(user__id=uid)
            for poll in polls:

                questions = poll.questions.all()
                for question in questions:

                    if question.type == 'text':
                        print('Question {}: Answer {}'.format(question.text, question.text_answer.text))

                    if question.type == 'sc':
                        try:
                            print('Question {}: selected choice {}'.format(question.text, question.selected_answer.choice.name))
                        except ObjectDoesNotExist:
                            ...

                    if question.type == 'mc':
                        ...
            serializer = {}
        else:
            poll = poll.filter(is_active=True)
            serializer = PollSerializer(poll, many=True).data

        return Response(serializer)

    def post(self, request):
        ...
