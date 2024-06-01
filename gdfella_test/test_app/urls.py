from django.urls import path
from .views import LoginView, CheckLoginView, GetMessagesView, SendMessageView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('check/login/', CheckLoginView.as_view(), name='check-login'),
    path('messages/', GetMessagesView.as_view(), name='get-messages'),
    path('messages/send/', SendMessageView.as_view(), name='send-message'),
]
