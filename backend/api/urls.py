from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BandViewSet, PostViewSet, TagViewSet, InstrumentViewSet


router = DefaultRouter()
router.register(r'bands', BandViewSet, basename='bands')
router.register(r'instruments', InstrumentViewSet, basename='instruments')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls))
]
