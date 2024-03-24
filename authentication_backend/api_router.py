from rest_framework.routers import DefaultRouter, SimpleRouter
from user_management.api.views import UserListSerializer, UserListViewSet

router = SimpleRouter()
router.register("user", UserListViewSet)

app_name = "api"
urlpatterns = router.urls
