from django.db import models
from django.contrib.auth.models import User

from datetime import time
import pytz
from jdatetime import datetime


class TelUser(models.Model):
    chat_id = models.IntegerField(verbose_name='Chat ID', unique=True)
    first_name = models.CharField(
        verbose_name='First Name', blank=True, max_length=150)
    last_name = models.CharField(
        verbose_name='Last Name', blank=True, max_length=150)
    tel_username = models.CharField(
        verbose_name='Telegram Username', blank=True,
        max_length=150)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.chat_id} - {self.first_name}'


class QuestionType(models.Model):
    name = models.CharField(verbose_name='Type Name', max_length=100)
    text = models.TextField(verbose_name='Question Text', max_length=350)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    qtype = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    message_id = models.IntegerField(verbose_name='Message ID', unique=True)
    date_asked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.qtype)} - {self.message_id}'



class AnswerManager(models.Manager):
    def all_by_date(self, jalali=False):
        res = []
        res2 = []
        dates = []

        for a in self.all():
            if a.answer_date.date() not in dates:
                dates.append(a.answer_date.date())

        for date in dates:
            every = []
            for a in self.all():
                if a.answer_date.date() == date:
                    every.append(a)
            if jalali:
                date = datetime.fromgregorian(date=date)
            res.append((date, every))
            res2.append(every)

        return (res, res2)


class Answer(models.Model):
    answer_choices = [
        ('NO', 'No'),
        ('YS', 'Yes'),
    ]
    answer = models.CharField(
        verbose_name='Answer',
        max_length=2,
        choices=answer_choices)

    user = models.ForeignKey(TelUser, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

    answer_date = models.DateTimeField(
        verbose_name='Answer Date',
        auto_now=True)

    objects = AnswerManager()

    def tehranize(self):
        return self.answer_date.astimezone(tz=pytz.timezone('Asia/Tehran'))

    def day_or_night(self):
        t = self.tehranize().time()
        if time(hour=4) < t < time(hour=18):
            return "D"
        return "N"

    def __str__(self):
        return f'{self.answer} - {self.pk}'


class DetailedQuestion(models.Model):
    answer = models.TextField(max_length=300, null=True, blank=True)
    question = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    qid = models.IntegerField(unique=True)
    user = models.ForeignKey(TelUser, on_delete=models.CASCADE,
        null=True, blank=True)
    date_asked = models.DateTimeField(auto_now_add=True)
    date_answered = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.answer} - {self.qid}'
