from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from .models import Poll, Question, Choice, CompletedPoll
from .helpers import get_or_none


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
    choice = ChoiceSerializer(read_only=True)

    class Meta:
        model = CompletedPoll
        fields = ('id', 'completed_date', 'text', 'choice')


class QuestionAnswerSerializer(ModelSerializer):

    completed_question = CompletedPollSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'completed_question')


class GetPollSerializer(ModelSerializer):

    questions = QuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('name', 'questions')


class PostCompletedPollSerializer(ModelSerializer):

    class Meta:
        model = CompletedPoll
        fields = ('user_id', 'poll_id', 'question_id', 'choice_id', 'text', 'completed_date')

    def create(self, validated_data):
        poll = get_or_none(Poll, id=validated_data['poll_id'])
        user = get_or_none(User, id=validated_data['user_id'])
        question = get_or_none(Question, id=validated_data['question_id'])

        text = validated_data['text']

        if isinstance(validated_data['choice_id'], list):
            completed_polls = []
            choices = validated_data['choice_id']

            for _choice_id in choices:
                choice = get_or_none(Choice, id=_choice_id)
                completed_polls.append(CompletedPoll(poll=poll, user=user,
                                                     question=question, choice=choice))

            CompletedPoll.objects.bulk_create(completed_polls)

        else:
            choice = get_or_none(Choice, id=validated_data['choice_id'])
            CompletedPoll.objects.create(poll=poll, user=user,
                                         question=question, choice=choice,
                                         text=text)
        return CompletedPoll.objects.filter(poll__id=poll.id, user__id=user.id)
