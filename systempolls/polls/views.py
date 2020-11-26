from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import CompletedPoll, Poll, Choice, Question
from .services import get_result_poll


class PollView(APIView):
    """Получение активных опросов, пройденных опросов по ID, прохождение опросов по ID"""

    def get(self, request, uid=None) -> Response:

        if request.path == '/take/survey/':
            return Response({'message': 'use post method'})

        result = get_result_poll(uid)
        return Response(result)

    def post(self, request) -> Response:
        completed_polls = []
        data = request.data

        questions = data['questions']

        try:
            poll = Poll.objects.get(id=data['poll_id'])
        except ObjectDoesNotExist:
            return Response({'message': 'invalid data'}, status=400)

        try:
            user = User.objects.get(id=data['uid'])
        except ObjectDoesNotExist:
            user = None

        for question in questions:
            try:
                q = Question.objects.get(id=question['question_id'])
            except ObjectDoesNotExist:
                return Response({'message': 'invalid data'}, status=400)

            type_question = question['type']
            answer = question['answer']

            if type_question == 'text':
                completed_polls.append(CompletedPoll(user=user, poll=poll, question=q, text=answer))

            if type_question == 'sc':
                try:
                    choice = Choice.objects.get(id=answer)
                except ObjectDoesNotExist:
                    return Response({'message': 'invalid data'}, status=400)

                completed_polls.append(CompletedPoll(user=user, poll=poll, question=q, choice=choice))

            if type_question == 'mc':
                choices = Choice.objects.filter(id__in=answer)
                for choice in choices:
                    completed_polls.append(CompletedPoll(user=user, poll=poll, question=q, choice=choice))

        CompletedPoll.objects.bulk_create(completed_polls)

        return Response({"status": 200})
