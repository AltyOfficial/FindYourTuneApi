from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BandViewSet, InstrumentCategoryViewSet, InstrumentViewSet,
                    PostViewSet, RequestViewSet, TagViewSet)


router = DefaultRouter()
router.register(r'bands', BandViewSet, basename='bands')
router.register(r'instruments', InstrumentViewSet, basename='instruments')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'requests', RequestViewSet, basename='requests')
router.register(
    r'instrument_categories',
    InstrumentCategoryViewSet,
    basename='instrument_categories'
)


urlpatterns = [
    path('', include(router.urls))
]
