from django.db import models
from django.contrib.auth.models import User


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


class Answer(models.Model):
    answer_choices = [
        ('NO', 'No'),
        ('YS', 'Yes'),
    ]
    answer = models.CharField(
        verbose_name='Answer',
        max_length=2,
        choices=answer_choices)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer_date = models.DateTimeField(
        verbose_name='Answer Date',
        auto_now=True)

    def __str__(self):
        return f'{self.answer} - {self.pk}'
