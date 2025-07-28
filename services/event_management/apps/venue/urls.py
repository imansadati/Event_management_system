from rest_framework.routers import DefaultRouter
from .apis import VenueGetwayApiViewset


router = DefaultRouter()
router.register('venues', VenueGetwayApiViewset, basename='venue')

urlpatterns = router.urls
