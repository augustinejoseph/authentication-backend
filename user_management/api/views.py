from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
)
from rest_framework.generics import GenericAPIView
from .serializers import UserListSerializer, UserCreateSerializer, UserLoginSerializer
from rest_framework.response import Response
from user_management.models import User
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
)
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.models import TokenUser


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
        email = request.data.get("email")
        mobile = request.data.get("phone_number")
        response = {}
        if User.objects.filter(email=email).exists():
            response.update(
                {"error": "User with this email already exists."},
                status=HTTP_400_BAD_REQUEST,
            )
            return Response(response)
        if User.objects.filter(phone_number=mobile).exists():
            response.update(
                {"error": "User with this mobile already exists."},
                status=HTTP_400_BAD_REQUEST,
            )
            return Response(response)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response.update(
            {
                "message": "User created successfully",
            },
            status=HTTP_201_CREATED,
        )
        return Response(response)

    @action(
        methods=["POST"],
        detail=False,
        url_path="login",
        url_name="login",
        permission_classes=[AllowAny],
    )
    def login(self, request):
        response = {}
        email = request.data.get("email")
        mobile = request.data.get("mobile")
        password = request.data.get("password")

        if not email and not mobile:
            response.update(
                {"error": "Please provide either mobile or email"},
                status=HTTP_404_NOT_FOUND,
            )
            return Response(response)

        user = None
        if email:
            try:
                user = User.objects.get(email=request.data.get("email"))
            except User.DoesNotExist:
                response.update(
                    {"error": "User does not exist"}, status=HTTP_404_NOT_FOUND
                )

                return Response(response)
        else:
            try:
                user = User.objects.get(phone_number=request.data.get("mobile"))
            except User.DoesNotExist:
                response.update(
                    {"error": "User does not exist"}, status=HTTP_404_NOT_FOUND
                )

                return Response(response)
        if user:
            if check_password(password, user.password):
                token = RefreshToken.for_user(user)
                serializer = UserLoginSerializer(user)
                response.update(
                    {
                        "message": "Authentication successfull",
                        "token": str(token.access_token),
                        "refresh": str(token),
                        "user_info": str(serializer.data),
                    },
                    status=HTTP_200_OK,
                )

                return Response(response)
            else:
                response.update(
                    {"error": "Password is wrong"},
                    status=HTTP_404_NOT_FOUND,
                )
                return Response(response)

        else:
            response.append({"error": "User does not exist"})
            return Response(response, status=HTTP_404_NOT_FOUND)

    @action(
        methods=["POST"],
        detail=False,
        url_path="logout",
        url_name="logout",
    )
    def logout(self, request):
        try:
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                response = {"error": "Refresh token is required"}
                return Response(response, status=HTTP_400_BAD_REQUEST)

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError as e:
                response = {"error": str(e)}
                return Response(response, status=HTTP_400_BAD_REQUEST)

            response = {"message": "Logout successful"}
            return Response(response, status=HTTP_200_OK)

        except Exception as e:
            response = {"error": "Something went wrong during logout"}
            return Response(response, status=HTTP_500_INTERNAL_SERVER_ERROR)
