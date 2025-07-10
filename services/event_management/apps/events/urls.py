from rest_framework.routers import DefaultRouter
from .apis import EventGetwayApiViewSet

router = DefaultRouter()
router.register('events', EventGetwayApiViewSet, basename='event')

urlpatterns = router.urls
