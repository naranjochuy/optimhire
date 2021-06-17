from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(max_length=100)

    @property
    def object(self):
        return self.validated_data
