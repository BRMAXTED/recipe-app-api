"""
Serializers for the user API View
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as gt
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data: dict):
        """
        Create and return a user with encripted password
        """
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user auth token
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},  # This will replace text
        trim_whitespace=False,
        )

    def validate(self, attrs):
        """
        Validate and authenticate the user
        """
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = gt('Unable to authenticate with provided credentials')
            # Will cause 400 bad request, which we want
            raise serializers.ValidationError(msg, code='authorication')

        attrs['user'] = user
        return attrs


