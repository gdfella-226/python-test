from django.db import models


class User(models.Model):
    username = models.CharField(max_length=15, unique=True)
    status = models.CharField(max_length=20, default='waiting_qr_login')


class Message(models.Model):
    username = models.CharField(max_length=100)
    is_self = models.BooleanField(default=False)
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
