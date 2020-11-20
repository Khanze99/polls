from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Poll(models.Model):
    name = models.CharField(max_length=511)
    start_date = models.DateTimeField(editable=False, auto_now_add=timezone.now)
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='completed_polls')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if timezone.now() < self.end_date:
            self.is_active = True

        super(Poll, self).save(force_insert=force_insert, force_update=force_update,
                               using=using, update_fields=update_fields)


class Question(models.Model):
    answer_type = (
        ('text', 'Ответ в виде текста'),
        ('sc', 'Ответ с выбором одного варианта'),
        ('mc', 'Ответ с выбором нескольких вариантов')
    )

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=1000, verbose_name='Text question')
    type = models.CharField(max_length=4, choices=answer_type)

    def __str__(self):
        return self.text

    def get_selected_answers(self):
        return [selected_answer.choice for selected_answer in self.selected_answers.all()]


class Choice(models.Model):
    name = models.CharField(max_length=300, verbose_name='Text choice')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')

    def __str__(self):
        return self.name


class TextAnswer(models.Model):
    text = models.TextField(verbose_name='Answer question')
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='text_answer')


class ChoiceAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='selected_answer')
    choice = models.OneToOneField(Choice, on_delete=models.CASCADE)


class MultiChoiceAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='selected_answers')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

