from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll
from .serializers import PollSerializer
from .services import get_result_poll


class PollView(APIView):
    """Получение активных опросов, пройденных опросов по ID, прохождение опросов по ID"""

    def get(self, request, uid=None) -> Response:

        if request.path == '/take/survey/':
            return Response({'message': 'use post method'})

        result = get_result_poll(uid)
        return Response(result)

    def post(self, request):
        print(request.data)
        return Response({"message": "you too"})
