from rest_framework.serializers import ModelSerializer

from .models import Poll, Question, Choice, TextAnswer, ChoiceAnswer, MultiChoiceAnswer


class ChoiceAnswerSerializer(ModelSerializer):

    class Meta:
        model = ChoiceAnswer
        fields = '__all__'


class MultiChoiceAnswerSerializer(ModelSerializer):

    class Meta:
        model = MultiChoiceAnswer
        fields = '__all__'


class TextAnswerSerializer(ModelSerializer):

    class Meta:
        model = TextAnswer
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



