from rest_framework.routers import DefaultRouter
from .apis import SpeakerGetwayApiViewset


router = DefaultRouter()
router.register('speakers', SpeakerGetwayApiViewset, basename='speaker')

urlpatterns = router.urls
