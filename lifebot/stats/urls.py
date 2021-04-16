from django.urls import path

from .views import Result, AllRES

app_name = 'stats'

urlpatterns = [
    path('<int:chat_id>', Result.as_view(), name='result'),
    path('all', AllRES.as_view(), name='all'),
]
