from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User

from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.generics import \
    RetrieveUpdateDestroyAPIView, ListAPIView, ListAPIView

from .models import QuestionType, Question, Answer
from .serializers import QuestionSerializer, \
    QuestionTypeSerializer, AnswerSerializer


class Index(APIView):
    def get(self, request):
        return Response("Hello bitch")


class QuestionView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer

    def get_object(self):
        kw = self.kwargs
        return get_object_or_404(Question, message_id=kw['message_id'])


class QuestionTypeView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionTypeSerializer

    def get_object(self):
        kw = self.kwargs
        if 'pk' in kw:
            return get_object_or_404(QuestionType, pk=kw['pk'])
        elif 'name' in kw:
            return get_object_or_404(QuestionType, name=kw['name'])


class QuestionTypeListView(ListAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer


class AnswerView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer

    def get_object(self):
        mid = self.kwargs['message_id']
        quest = get_object_or_404(Question, message_id=mid)
        return get_object_or_404(Answer, question=quest)


class AnswerUserView(ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        username = str(self.kwargs['username'])
        user = get_object_or_404(User, username=username)
        return get_list_or_404(Answer, user=user)
