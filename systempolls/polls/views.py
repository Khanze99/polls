from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll
from .serializers import PollSerializer

# Create your views here.


class PollView(APIView):

    def get(self, request):
        poll = Poll.objects.filter(is_active=True)
        serializer = PollSerializer(poll, many=True).data
        return Response(serializer)
