from django.urls import path, include
import core.api.users as users_routes

urlpatterns = [
    path('', include(users_routes)),
]