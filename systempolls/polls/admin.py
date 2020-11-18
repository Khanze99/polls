from django.contrib import admin


from .models import Poll, Question, \
    ChoiceAnswer, TextAnswer,\
    MultiChoiceAnswer, Choice


class QuestionInline(admin.TabularInline):
    model = Question


class ChoiceInline(admin.TabularInline):
    model = Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):
        model = self.model
        obj = self.get_object(request, object_id)

        if obj.type == 'sc' or obj.type == 'mc':
            self.inlines = [ChoiceInline, ]
        
        return super(QuestionAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(TextAnswer)
admin.site.register(ChoiceAnswer)
admin.site.register(MultiChoiceAnswer)
