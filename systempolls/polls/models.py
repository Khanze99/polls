from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Poll(models.Model):
    name = models.CharField(max_length=511)
    start_date = models.DateTimeField(editable=False, auto_now_add=timezone.now)
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='completed_polls')

    def __str__(self):
        return self.name


class Question(models.Model):
    answer_type = (
        ('tx', 'Ответ в виде текста'),
        ('sc', 'Ответ с выбором одного варианта'),
        ('mc', 'Ответ с выбором нескольких вариантов')
    )

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=1000, verbose_name='Text question')
    type = models.CharField(max_length=2, choices=answer_type)

    def __str__(self):
        return self.text


class TextAnswer(models.Model):
    text = models.TextField(verbose_name='Answer question')
    question = models.OneToOneField(Question, on_delete=models.CASCADE)


class Choice(models.Model):
    text = models.CharField(max_length=300, verbose_name='Text choice')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class ChoiceAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='selected_answer')
    choice_id = models.OneToOneField(Choice, on_delete=models.CASCADE)


class MultiChoiceAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='selected_answers')
    choice_id = models.ForeignKey(Choice, on_delete=models.CASCADE)

