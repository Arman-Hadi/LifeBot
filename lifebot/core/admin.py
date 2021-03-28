from django.contrib import admin

from .models import Question, QuestionType, Answer, TelUser


@admin.register(TelUser)
class TelUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'first_name', 'last_name', 'tel_username')
    search_fields = ('first_name', 'chat_id', 'last_name', 'tel_username')
    list_filter = ('date_joined',)


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'date_updated')
    search_fields = ('name', 'text')
    list_filter = ('date_updated',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'qtype', 'message_id','date_asked')
    search_fields = ('qtype', 'message_id')
    list_filter = ('date_asked',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'answer', 'user', 'question')
    search_fields = ('answer', 'user', 'question')
    list_filter = ('answer_date',)
