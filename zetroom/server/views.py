from django.shortcuts import render
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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


class ApplicationView(generics.ListAPIView):
    queryset = Application.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ApplicationListSerializer


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = GroupListSerializer

    # def get_serializer_context(self):
    #     return super().get_serializer_context().update({'account_tg': self.request.data['account']})


class Onlu(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ApplicationCreateAPI(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)
