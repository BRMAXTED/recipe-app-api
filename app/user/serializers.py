"""
Serializers for the user API View
"""
from typing import override
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.utils.translation import gettext as gt
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object
    """

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    @override
    def create(self, validated_data: dict) -> AbstractBaseUser:
        """
        Create and return a user with encripted password
        """
        return get_user_model().objects.create_user(**validated_data)

    @override
    def update(self, instance: User, validated_data: dict) -> AbstractBaseUser:
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user auth token
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},  # This will replace text
        trim_whitespace=False,
        )

    @override
    def validate(self, attrs: dict) -> dict:
        """
        Validate and authenticate the user
        """
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            msg = gt('Unable to authenticate with provided credentials')
            # Will cause 400 bad request, which we want
            raise serializers.ValidationError(msg, code='authorication')

        attrs['user'] = user
        return attrs
