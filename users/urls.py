from rest_framework.routers import DefaultRouter

from .views import AuthViewSet

router = DefaultRouter()
router.register('', AuthViewSet)

urlpatterns = router.urls
