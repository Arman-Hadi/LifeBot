from django.urls import path

from .views import Index, QuestionView, \
    QuestionTypeView, QuestionTypeListView, AnswerUserView, \
        AnswerView

app_name = 'core'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('q/<int:message_id>',
        QuestionView.as_view(), name='quest-mid'),
    path('qtype/<int:pk>',
        QuestionTypeView.as_view(), name='qtype-pk'),
    path('qtype/<slug:name>',
        QuestionTypeView.as_view(), name='qtype-name'),
    path('qtype-list',
        QuestionTypeListView.as_view(), name='qtype-list'),
    path('answer/<int:message_id>',
        AnswerView.as_view(), name='answer'),
    path('user-answers/<int:username>',
        AnswerUserView.as_view(), name='user-answers'),
]
