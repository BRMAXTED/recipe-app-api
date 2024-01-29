"""
Views for the client API
"""

from rest_framework import (
    authentication,
    permissions,
    viewsets)
from client.serializers import (
    ClientSerializer,
    )


class ClientViewSet(viewsets.ModelViewSet):
    """
    View for managing clients
    """
    serializer_class = ClientSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
