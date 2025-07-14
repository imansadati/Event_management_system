from rest_framework.routers import DefaultRouter
from .apis import EventGetwayApiViewSet, EventCategoryGetwayApiViewSet

router = DefaultRouter()
router.register('events', EventGetwayApiViewSet, basename='event')
router.register('categories',
                EventCategoryGetwayApiViewSet, basename='category')

urlpatterns = router.urls
