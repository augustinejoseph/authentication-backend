from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_management.api.views import UserViewSet

router = DefaultRouter()
router.register("user", UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
