from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import User

from .models import Poll, Question, Choice, CompletedPoll


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ChoiceSerializer(ModelSerializer):

    class Meta:
        model = Choice
        fields = ('id', 'name')


class QuestionSerializer(ModelSerializer):

    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'choices')


class PollSerializer(ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'name', 'end_date', 'questions')


class CompletedPollSerializer(ModelSerializer):

    class Meta:
        model = CompletedPoll
        fields = '__all__'


