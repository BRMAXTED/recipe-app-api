"""
URL mapping for the client app
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from client import views

router = DefaultRouter()
router.register('clients', views.ClientViewSet, basename='clients')

app_name = 'client'

urlpatterns = [
    path('', include(router.urls))
]
