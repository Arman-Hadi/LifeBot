from django.urls import path

from .views import telegram_webhook, secret


app_name = 'core'

urlpatterns = [
    path(f'{secret}/', telegram_webhook, name='telegram-webhook')
]
