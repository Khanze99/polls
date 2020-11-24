from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import CompletedPoll, CompletedQuestion, Answer, Poll, Choice, Question
from .services import get_result_poll


class PollView(APIView):
    """Получение активных опросов, пройденных опросов по ID, прохождение опросов по ID"""

    def get(self, request, uid=None) -> Response:

        if request.path == '/take/survey/':
            return Response({'message': 'use post method'})

        result = get_result_poll(uid)
        return Response(result)

    def post(self, request) -> Response:
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

        completed_poll = CompletedPoll.objects.create(poll=poll, user=user)

        for question in questions:
            try:
                q = Question.objects.get(id=question['question_id'])
            except ObjectDoesNotExist:
                return Response({'message': 'invalid data'}, status=400)

            type_question = question['type']
            answer = question['answer']

            completed_question = CompletedQuestion.objects.create(completed_poll=completed_poll, question=q)

            if type_question == 'text':
                Answer.objects.create(completed_question=completed_question, text=answer)

            if type_question == 'sc':
                try:
                    choice = Choice.objects.get(id=answer)
                except ObjectDoesNotExist:
                    return Response({'message': 'invalid data'}, status=400)

                Answer.objects.create(completed_question=completed_question, choice=choice)

            if type_question == 'mc':
                choices = Choice.objects.filter(id__in=answer)
                for choice in choices:
                    Answer.objects.create(completed_question=completed_question, choice=choice)

        return Response({"status": 200})
