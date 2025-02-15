from rest_framework.routers import DefaultRouter
from professionals.api import ProfessionalViewSet

router = DefaultRouter()
router.register(r'professionals', ProfessionalViewSet, basename='user')
urlpatterns = router.urls