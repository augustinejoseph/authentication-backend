from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
)
from rest_framework.generics import GenericAPIView
from .serializers import UserListSerializer, UserCreateSerializer
from rest_framework.response import Response
from user_management.models import User
from rest_framework.status import HTTP_201_CREATED
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        if self.action == "retrieve":
            return UserListSerializer
        if self.action == "create":
            return UserCreateSerializer
        if self.action == "update":
            return UserListSerializer
        if self.action == "partial_update":
            return UserListSerializer
        if self.action == "destroy":
            return UserListSerializer
        return UserListSerializer

    def get_queryset(self, *args, **kwargs):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)
