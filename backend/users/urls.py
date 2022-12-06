from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, InviteViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'invites', InviteViewSet, basename='invites')

urlpatterns = [
    path('', include(router.urls))
]
