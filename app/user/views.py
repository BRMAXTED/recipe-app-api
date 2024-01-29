"""
Views for the user API
"""
from typing import override
from django.contrib.auth import get_user_model
from rest_framework import (
    generics,
    authentication,
    permissions,
    viewsets)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user import serializers


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    """
    serializer_class = serializers.UserDetailAdminSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]


class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for user
    """
    serializer_class = serializers.AuthTokenSerializer
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user
    """
    serializer_class = serializers.UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @override
    def get_object(self):
        """
        Retrieve and return the authenticated user
        """
        return self.request.user


class AdminManageViewSet(viewsets.ModelViewSet):
    """
    Manage a user as the admin
    """
    serializer_class = serializers.UserDetailAdminSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'list':
            return serializers.AdminSerialiser
        return self.serializer_class

    # def get(self, request, *args, **kwargs):
    #     breakpoint()
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     breakpoint()
    #     x = self.update(request, *args, **kwargs)

    #     return x

    # def patch(self, request, *args, **kwargs):
    #     breakpoint()
    #     return self.partial_update(request, *args, **kwargs)

    # @override
    # def get_object(self, validated_data):
    #     """
    #     Retrieve and return the user specified by the id
    #     """
    #     _id = validated_data.pop('id', None)
    #     try:
    #         user_instance = User.objects.filter(pk=_id).get()
    #     except instance.DoesNotExist:
    #         normal_msg = f'Unable to retrieve user with provided id: {_id}'
    #         msg = gt(normal_msg)
    #         # Will cause 400 bad request, which we want
    #         raise serializers.ValidationError(msg, code='Bad User ID')
    #     return self.request.user
