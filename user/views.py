from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import SignUpSerializer, LoginSerializer
from .utils import generate_token
from rest_framework.permissions import AllowAny


class SignUpView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        serializers = SignUpSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        token = generate_token(user)

        return Response({"token": token}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        serializers = LoginSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        return Response(serializers.validated_data["token"], status=status.HTTP_200_OK)

