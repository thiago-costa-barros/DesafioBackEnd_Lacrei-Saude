from django.urls import path, include
import core.api.users as users_routes
import core.api.professionals as professionals_routes
import core.api.appointments as appointments_routes

urlpatterns = [
    path('', include(users_routes)),
    path('', include(professionals_routes)),
    path('', include(appointments_routes))
]