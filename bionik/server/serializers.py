from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import requests

url = "https://api.telegram.org/bot5346235377:AAGg1mWc4FPRxGn1GFcnOBcj75MMLlrAJlA/sendMessage"


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Account.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'tg')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'tg': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Account.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            tg=validated_data['tg']
        )

        user.set_password(validated_data['password'])
        user.save()
        payload = {
            "text": f"Вы успешно зарегистрировались\nВаш никнейм {validated_data['username']}\nВаш пароль {validated_data['password'][0:3]}{(len(validated_data['password'])-3)*'*'}",
            "chat_id": validated_data['tg'],
        }
        response = requests.post(url, json=payload)
        return user


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', ]

