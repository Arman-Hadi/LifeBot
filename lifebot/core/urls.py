from django.urls import path

from .views import Index, QuestionView, \
    QuestionTypeView, QuestionTypeListView, AnswerUserView, \
        AnswerView, AnswerCreateView, UserView, UserCreateView, \
            QuestionCreateView, UserListView, CreateAuthToken

app_name = 'core'

urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('q/<int:message_id>',
        QuestionView.as_view(), name='quest-mid'),
    path('q-create',
        QuestionCreateView.as_view(), name='quest-create'),

    path('qtype/<int:pk>',
        QuestionTypeView.as_view(), name='qtype-pk'),
    path('qtype/<slug:name>',
        QuestionTypeView.as_view(), name='qtype-name'),
    path('qtype-list',
        QuestionTypeListView.as_view(), name='qtype-list'),

    path('answer/<int:message_id>',
        AnswerView.as_view(), name='answer'),
    path('user-answers/<int:chat_id>',
        AnswerUserView.as_view(), name='user-answers'),
    path('create-answer',
        AnswerCreateView.as_view(), name='create-answer'),

    path('user/<int:chat_id>',
        UserView.as_view(), name='user'),
    path('user-create',
        UserCreateView.as_view(), name='user-create'),
    path('user-list',
        UserListView.as_view(), name='user-list'),

    path('token',
        CreateAuthToken.as_view(), name='token'),
]
