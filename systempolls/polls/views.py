from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_result_poll, save_results


class PollView(APIView):
    """Получение активных опросов, пройденных опросов по ID, прохождение опросов по ID"""

    def get(self, request, uid=None) -> Response:

        if request.path == '/take/survey/':
            return Response({'message': 'use post method'})

        result = get_result_poll(uid)
        return Response(result)

    def post(self, request) -> Response:
        data = request.data
        save_results(data)
        return Response({'status': 'created'}, status=201)
