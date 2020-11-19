from rest_framework.serializers import ModelSerializer

from .models import Poll, Question, Choice


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
