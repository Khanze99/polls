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


class PollWithoutQuestionsSerializer(ModelSerializer):

    class Meta:
        model = Poll
        fields = '__all__'


class QuestionWithoutChoicesSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class CompletedPollSerializer(ModelSerializer):

    user = UserSerializer()
    poll = PollWithoutQuestionsSerializer()
    question = QuestionWithoutChoicesSerializer()
    choice = ChoiceSerializer()

    class Meta:
        model = CompletedPoll
        fields = ('user', 'poll', 'question', 'choice', 'text', 'completed_date')


