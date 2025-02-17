from django.urls import path, include
import core.api.users as users_routes
import core.api.professionals as professionals_routes

urlpatterns = [
    path('', include(users_routes)),
    path('', include(professionals_routes))
]