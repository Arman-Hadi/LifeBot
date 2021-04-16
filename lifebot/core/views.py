from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import serializers

from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.generics import \
    RetrieveUpdateDestroyAPIView, ListAPIView, \
        ListAPIView, CreateAPIView, ListAPIView
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import QuestionType, Question, Answer, TelUser, DetailedQuestion
from .serializers import QuestionSerializer, \
    QuestionTypeSerializer, AnswerSerializer, UserSerializer, \
        AuthTokenSerializer, DetailedQuestionSerializer


class Index(APIView):
    def get(self, request):
        return Response("Hello, Welcome to LifeBot API!")


class QuestionView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        kw = self.kwargs
        return get_object_or_404(Question, message_id=kw['message_id'])


class QuestionCreateView(CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


class QuestionTypeView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionTypeSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        kw = self.kwargs
        if 'pk' in kw:
            return get_object_or_404(QuestionType, pk=kw['pk'])
        elif 'name' in kw:
            return get_object_or_404(QuestionType, name=kw['name'])


class QuestionTypeListView(ListAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


class AnswerView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        mid = self.kwargs['message_id']
        quest = get_object_or_404(Question, message_id=mid)
        return get_object_or_404(Answer, question=quest)


class AnswerUserView(ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        chat_id = str(self.kwargs['chat_id'])
        user = get_object_or_404(TelUser, chat_id=chat_id)
        return get_list_or_404(Answer, user=user)


class AnswerCreateView(CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


class UserView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        kw = self.kwargs
        return get_object_or_404(TelUser, chat_id=kw['chat_id'])


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = TelUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


class CreateAuthToken(ObtainAuthToken):
    """Create token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class DetailedQuestionView(RetrieveUpdateDestroyAPIView):
    serializer_class = DetailedQuestionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        kw = self.kwargs
        return get_object_or_404(DetailedQuestion, qid=kw['qid'])


class DetailedQuestionCreate(CreateAPIView):
    serializer_class = DetailedQuestionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)
