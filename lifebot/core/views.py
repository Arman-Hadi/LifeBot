from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.generics import \
    RetrieveUpdateDestroyAPIView, ListAPIView, \
        ListAPIView, CreateAPIView

from .models import QuestionType, Question, Answer, TelUser
from .serializers import QuestionSerializer, \
    QuestionTypeSerializer, AnswerSerializer, UserSerializer


class Index(APIView):
    def get(self, request):
        return Response("Hello bitch")


class QuestionView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer

    def get_object(self):
        kw = self.kwargs
        return get_object_or_404(Question, message_id=kw['message_id'])


class QuestionCreateView(CreateAPIView):
    serializer_class = QuestionSerializer


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
        chat_id = str(self.kwargs['chat_id'])
        user = get_object_or_404(TelUser, chat_id=chat_id)
        return get_list_or_404(Answer, user=user)


class AnswerCreateView(CreateAPIView):
    serializer_class = AnswerSerializer


class UserView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        kw = self.kwargs
        return get_object_or_404(TelUser, chat_id=kw['chat_id'])


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
