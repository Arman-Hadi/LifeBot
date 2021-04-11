from django.urls import path

from .views import Result

app_name = 'stats'

urlpatterns = [
    path('<int:chat_id>', Result.as_view(), name='result')
]
