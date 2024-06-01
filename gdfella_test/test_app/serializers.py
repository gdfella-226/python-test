from rest_framework import serializers
from .models import User, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'status']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['username', 'is_self', 'message_text', 'created_at']
