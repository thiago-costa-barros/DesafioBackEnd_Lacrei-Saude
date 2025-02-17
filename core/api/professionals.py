from rest_framework.routers import DefaultRouter
from professionals.api import HealthProfessionalViewSet, ProfessionViewSet

router = DefaultRouter()
router.register(r'healthprofessional', HealthProfessionalViewSet, basename='healthprofessional')
router.register(r'profession', ProfessionViewSet, basename='profession')

urlpatterns = router.urls