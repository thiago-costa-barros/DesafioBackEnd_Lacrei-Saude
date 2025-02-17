from rest_framework.routers import DefaultRouter
from appointments.api import AppointmentModelViewSet

router = DefaultRouter()
router.register(r'appointment', AppointmentModelViewSet, basename='appointment')
urlpatterns = router.urls