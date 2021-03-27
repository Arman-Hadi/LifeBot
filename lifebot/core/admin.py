from django.contrib import admin

from .models import Question, QuestionType, Answer


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_updated')
    search_fields = ('name', 'text')
    list_filter = ('date_updated',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qtype', 'message_id','date_asked')
    search_fields = ('qtype', 'message_id')
    list_filter = ('date_asked',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user', 'question')
    search_fields = ('answer', 'user', 'question')
    list_filter = ('answer_date',)
