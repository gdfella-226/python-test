from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Message
from .serializers import UserSerializer, MessageSerializer
from .forms import LoginForm, CheckLoginForm, GetMessagesForm, SendMessageForm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render, redirect
from django.urls import reverse
import random
import string
# from tg_core import VIRTUAL_CLIENT

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: openapi.Response('QR Link', UserSerializer)}
    )
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            user, created = User.objects.get_or_create(phone=phone)
            qr_link_url = 'https://example.com/qr/' + ''.join(
                random.choices(string.ascii_letters + string.digits, k=10))
            return render(request, 'login.html', {'form': form, 'qr_link_url': qr_link_url})
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def get(self, request):
        form = CheckLoginForm()
        return render(request, 'login.html', {'form': form, 'status': status})


class CheckLoginView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('phone', openapi.IN_QUERY, description="Phone number", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response('Status', UserSerializer)}
    )
    def get(self, request):
        status = None
        if request.method == 'GET' and 'phone' in request.GET:
            form = CheckLoginForm(request.GET)
            if form.is_valid():
                phone = form.cleaned_data['phone']
                try:
                    user = User.objects.get(phone=phone)
                    status = user.status
                except User.DoesNotExist:
                    status = 'error'
        else:
            form = CheckLoginForm()
        return render(request, 'check_login.html', {'form': form, 'status': status})


class GetMessagesView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('phone', openapi.IN_QUERY, description="Phone number", type=openapi.TYPE_STRING),
            openapi.Parameter('uname', openapi.IN_QUERY, description="Username", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response('Messages', MessageSerializer(many=True))}
    )
    def get(self, request):
        messages = None
        if request.method == 'GET' and 'phone' in request.GET and 'uname' in request.GET:
            form = GetMessagesForm(request.GET)
            if form.is_valid():
                phone = form.cleaned_data['phone']
                uname = form.cleaned_data['uname']
                try:
                    user = User.objects.get(phone=phone)
                    for msg in external_messages:
                        Message.objects.create(user=user, username=msg['username'], message_text=msg['message_text'],
                                               is_self=msg['is_self'])
                    messages = user.messages.filter(username=uname).order_by('-created_at')[:50]
                except User.DoesNotExist:
                    messages = []
        else:
            form = GetMessagesForm()
        return render(request, 'messages.html', {'form': form, 'messages': messages})


class SendMessageView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message_text': openapi.Schema(type=openapi.TYPE_STRING),
                'from_phone': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: openapi.Response('Status', UserSerializer)}
    )
    def post(self, request):
        status = None
        if request.method == 'POST':
            form = SendMessageForm(request.POST)
            if form.is_valid():
                message_text = form.cleaned_data['message_text']
                from_phone = form.cleaned_data['from_phone']
                username = form.cleaned_data['username']
                try:
                    user = User.objects.get(phone=from_phone)
                    Message.objects.create(user=user, username=username, message_text=message_text, is_self=True)
                    status = 'ok'
                except User.DoesNotExist:
                    status = 'error'
        else:
            form = SendMessageForm()
        return render(request, 'send_message.html', {'form': form, 'status': status})

    def get(self, request):
        form = CheckLoginForm()
        return render(request, 'send_message.html', {'form': form, 'status': status})
