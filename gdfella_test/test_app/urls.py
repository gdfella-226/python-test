from django.urls import path
from .views import LoginView, CheckLoginView, GetMessagesView, SendMessageView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/check/', CheckLoginView.as_view(), name='check-login'),
    path('message/', GetMessagesView.as_view(), name='get-messages'),
    path('message/send/', SendMessageView.as_view(), name='send-message'),
]
