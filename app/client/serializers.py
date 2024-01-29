"""
Serializers for the Client API View
"""
from typing import override
from django.contrib.auth import (
    get_user_model,
    )
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.utils.translation import gettext as gt
from rest_framework import serializers

from core.models import BusinessClient


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object
    """

    class Meta:
        model = BusinessClient
        fields = ['name', 'date_created']
        extra_kwargs = {
            'name': {'required': True},
            'date_created': {'read_only': True}
        }

    @override
    def create(self, validated_data: dict) -> BusinessClient:
        """
        Create and return a user with encripted password
        """
        return BusinessClient.objects.create(**validated_data)

    @override
    def update(self,
               instance: BusinessClient,
               validated_data: dict) -> BusinessClient:
        client = super().update(instance, validated_data)
        client.save()
        return client


