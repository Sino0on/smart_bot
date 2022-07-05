from django.shortcuts import render
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AccountListSerializer


class SuperAccountListView(generics.ListAPIView):
    queryset = Account.objects.filter(is_staff=True)
    permission_classes = (AllowAny,)
    serializer_class = AccountListSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CourseListSerializer