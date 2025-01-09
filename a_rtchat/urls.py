from django.urls import path, include
from a_rtchat.views import *

urlpatterns = [
    path('chat', chat_view, name="chat"),
]