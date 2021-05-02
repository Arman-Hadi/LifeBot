import pytz

from django.contrib import admin
from django.utils import timezone

from .models import Question, QuestionType, Answer, TelUser, DetailedQuestion


def elapsed(date):
    elapsed = timezone.now() - date
    minute, second = divmod(elapsed.seconds, 60)
    hour, minute = divmod(minute, 60)
    year, day = divmod(elapsed.days, 365)
    if year > 0:
        return f'{year}y, {day}d'
    elif day==0 and hour==0 and minute==0:
        return f'Just Now!'
    else:
        return f'{day}d, {hour}h, {minute}m'

def tehranize(date):
    d = date.astimezone(tz=pytz.timezone('Asia/Tehran'))
    print(f'-------{d}-----')
    print(f'-------{date}-----')
    return d


@admin.register(TelUser)
class TelUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'first_name', 'last_name',
        'tel_username', 'in_tehran', 'elapsed_time', 'date_joined')
    search_fields = ('first_name', 'chat_id', 'last_name', 'tel_username')
    list_filter = ('date_joined',)

    def elapsed_time(self, obj):
        return elapsed(obj.date_joined)

    def in_tehran(self, obj):
        return tehranize(obj.date_joined)


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'in_tehran', 'elapsed_time', 'date_updated')
    search_fields = ('name', 'text')
    list_filter = ('date_updated',)

    def elapsed_time(self, obj):
        return elapsed(obj.date_updated)

    def in_tehran(self, obj):
        return tehranize(obj.date_updated)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'qtype', 'is_active', 'in_tehran',
        'elapsed_time', 'date_asked')
    search_fields = ('qtype', 'message_id')
    list_filter = ('date_asked', 'qtype')

    def elapsed_time(self, obj):
        return elapsed(obj.date_asked)

    def in_tehran(self, obj):
        return tehranize(obj.date_asked)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'answer', 'user', 'question',
        'in_tehran', 'elapsed_time', 'answer_date')
    search_fields = ('answer', 'user', 'question')
    list_filter = ('answer_date',)

    def elapsed_time(self, obj):
        return elapsed(obj.answer_date)

    def in_tehran(self, obj):
        return tehranize(obj.answer_date)


@admin.register(DetailedQuestion)
class DetailedQuestionAdmin(admin.ModelAdmin):
    list_display = ('qid', 'question', 'answer', 'user', 'is_active',
        'date_asked', 'date_answered')
    list_filter = ('question', 'date_asked', 'date_answered',)
    search_fields = ('user',)

    def ask_t(self, obj):
        return tehranize(obj.date_asked)

    def answer_t(self, obj):
        return tehranize(obj.date_answered)
