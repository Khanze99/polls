from django.contrib import admin


from .models import Poll, Question, \
    ChoiceAnswer, TextAnswer,\
    MultiChoiceAnswer, Choice


class QuestionInline(admin.TabularInline):
    model = Question


class ChoiceInline(admin.TabularInline):
    model = Choice


class TextAnswerInline(admin.TabularInline):
    model = TextAnswer


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):

    inlines = (QuestionInline,)


admin.site.register(Question)
admin.site.register(Choice)
