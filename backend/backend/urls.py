from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(  # new
    openapi.Info(
        title="FindYourTune API",
        default_version='v1',
        description="Dynamic Swagger API for FindYourTune Project",
        contact=openapi.Contact(email="alty.official.prim@gmail.com"),
    ),
    patterns=[path('api/', include('api.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(  # new
        'docs/',
        TemplateView.as_view(
            template_name='docs/swaggerui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'),
    re_path(  # new
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('users.urls')),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken'))
]


# urlpatterns += [
#     re_path(
#         r'^redoc/$',
#         schema_view.with_ui('redoc', cache_timeout=0),
#         name='schema-redoc'
#     ),
# ]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
