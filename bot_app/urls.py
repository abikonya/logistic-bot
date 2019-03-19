from django.conf.urls import url

from .views import UpdateBot

app_name = 'bot_app'

urlpatterns = [
    url(r'^827637721:AAHZAkFOMR3bSdLWhMvRktHvzR738zj2qdM/', UpdateBot.as_view(), name='update'),
]