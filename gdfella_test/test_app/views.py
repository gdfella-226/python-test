from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Message
from .serializers import UserSerializer, MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random
import string

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
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone=phone)
        qr_link_url = 'https://example.com/qr/' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return Response({'qr_link_url': qr_link_url})


class CheckLoginView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('phone', openapi.IN_QUERY, description="Phone number", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response('Status', UserSerializer)}
    )
    def get(self, request):
        phone = request.query_params.get('phone')
        if not phone:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
            return Response({'status': user.status})
        except User.DoesNotExist:
            return Response({'status': 'error'})


class GetMessagesView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('phone', openapi.IN_QUERY, description="Phone number", type=openapi.TYPE_STRING),
            openapi.Parameter('uname', openapi.IN_QUERY, description="Username", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response('Messages', MessageSerializer(many=True))}
    )
    def get(self, request):
        phone = request.query_params.get('phone')
        uname = request.query_params.get('uname')
        if not phone or not uname:
            return Response({'error': 'Phone number and username are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
            messages = user.messages.filter(username=uname).order_by('-created_at')[:50]
            serializer = MessageSerializer(messages, many=True)
            return Response({'messages': serializer.data})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


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
        message_text = request.data.get('message_text')
        from_phone = request.data.get('from_phone')
        username = request.data.get('username')
        if not message_text or not from_phone or not username:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=from_phone)
            Message.objects.create(user=user, username=username, message_text=message_text, is_self=True)
            return Response({'status': 'ok'})
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
