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
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'username': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'email': {'read_only': True},
            'password': {'write_only': True, 'min_length': 5}
        }

    @override
    def update(self, instance: User, validated_data: dict) -> AbstractBaseUser:
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)
            instance.save()
        return instance


class AdminSerialiser(serializers.ModelSerializer):
    """Base serializer for Admin Actions on Users"""

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_active',
                  'is_staff', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'min_length': 3},
            'password': {'write_only': True, 'min_length': 5}
        }


class UserDetailAdminSerializer(AdminSerialiser):
    """
    Serializer for viewing users as the admin
    """

    # class Meta(AdminSerialiser.Meta):
    #     fields = AdminSerialiser.Meta.fields + ['password']
    #     extra_kwargs = {
    #         'password': {'write_only': True, 'min_length': 5}
    #     }

    @override
    def create(self, validated_data: dict) -> AbstractBaseUser:
        """
        Create and return a user with encripted password
        """
        return get_user_model().objects.create_user(**validated_data)

# class UserAdminSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'username', 'first_name',
#                   'last_name', 'email', 'password',
#                   'is_active', 'is_staff']
#         extra_kwargs = {
#             'id': {'required': True},
#             'username': {'min_length': 3},
#             'password': {'write_only': True, 'min_length': 5}
#         }

#     @override
#     def update(self,
#                        instance: User,
#                        validated_data: dict,
#                        partial=False) -> AbstractBaseUser:
#         breakpoint()
#         _id = validated_data.pop('id', None)
#         try:
#             user_instance = User.objects.filter(pk=_id).get()
#         except instance.DoesNotExist:
#             normal_msg = f'Unable to retrieve user with provided id: {_id}'
#             breakpoint()
#             msg = gt(normal_msg)
#             # Will cause 400 bad request, which we want
#             raise serializers.ValidationError(msg, code='Bad User ID')

#         password = validated_data.pop('password', None)
#         if any([x for x in validated_data.values()]):
#             super().update(user_instance, validated_data)
#         if password:
#             user_instance.set_password(password)
#             user_instance.save()
#         return user_instance


# class UserAdminCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'username', 'first_name',
#                   'last_name', 'email', 'password',
#                   'is_active', 'is_staff']
#         extra_kwargs = {
#             'username': {'min_length': 3},
#             'password': {'write_only': True, 'min_length': 5}
#         }

#     @override
#     def create(self, validated_data: dict) -> AbstractBaseUser:
#         """
#         Create and return a user with encripted password
#         """
#         return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user auth token
    """
    username = serializers.CharField()
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
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
