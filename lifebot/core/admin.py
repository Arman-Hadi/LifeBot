from django.contrib import admin
from django.utils import timezone

from .models import Question, QuestionType, Answer, TelUser


def elapsed(date):
        elapsed = timezone.now() - date
        minute, second = divmod(elapsed.seconds, 60)
        hour, minute = divmod(minute, 60)
        year, day = divmod(elapsed.days, 365)
        if year > 0:
            return f'{year}y, {day}d'
        elif minute > 0:
            return f'{day}d, {hour}h, {minute}m'
        else:
            return f'Just Now!'


@admin.register(TelUser)
class TelUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'first_name', 'last_name',
        'tel_username', 'date_joined', 'elapsed_time')
    search_fields = ('first_name', 'chat_id', 'last_name', 'tel_username')
    list_filter = ('date_joined',)

    def elapsed_time(self, obj):
        return elapsed(obj.date_joined)


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'date_updated', 'elapsed_time')
    search_fields = ('name', 'text')
    list_filter = ('date_updated',)

    def elapsed_time(self, obj):
        return elapsed(obj.date_updated)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'qtype', 'message_id','date_asked',
        'elapsed_time')
    search_fields = ('qtype', 'message_id')
    list_filter = ('date_asked',)

    def elapsed_time(self, obj):
        return elapsed(obj.date_asked)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'answer', 'user', 'question',
        'answer_date', 'elapsed_time')
    search_fields = ('answer', 'user', 'question')
    list_filter = ('answer_date',)

    def elapsed_time(self, obj):
        return elapsed(obj.answer_date)
