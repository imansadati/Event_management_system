from rest_framework.routers import DefaultRouter
from .apis import OrganizerGetwayApiViewset


router = DefaultRouter()
router.register('organizers', OrganizerGetwayApiViewset, basename='organizer')

urlpatterns = router.urls
