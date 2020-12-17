from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from django.contrib.auth.models import User
from .serializers import RefreshTokenSerializer, UserSerializer
import json


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = ()

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            sz.create(sz.validated_data)
            return Response("Account created", status=status.HTTP_201_CREATED)
        return Response(sz.errors, status=status.HTTP_400_BAD_REQUEST)
