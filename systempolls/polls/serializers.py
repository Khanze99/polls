from rest_framework.serializers import ModelSerializer

from .models import Poll, Question, Choice


class ChocieSerializer(ModelSerializer):

    class Meta:
        model = Choice
        fields = ('text',)


class QuestionSerializer(ModelSerializer):
    choices = ChocieSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('text', 'type', 'choices')


class PollSerializer(ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'name', 'end_date', 'questions')