from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.shared.utils.decorators import superuser_required
from django.http import HttpResponse


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



def health(request):
    return HttpResponse("OK")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls.v1')),
    path('api/v2/', include('apps.urls.v2')),
    path("health/", health),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]


urlpatterns += [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Swagger & Redoc
if settings.DEBUG:
    urlpatterns += [
        path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name='schema'), name="swagger-ui"),
        path("api/v1/redoc/", SpectacularRedocView.as_view(url_name='schema'), name="redoc"),
    ]
else:
    urlpatterns += [
        path("api/v1/docs/", superuser_required(SpectacularSwaggerView.as_view(url_name='schema')), name="swagger-ui"),
        path("api/v1/redoc/", superuser_required(SpectacularRedocView.as_view(url_name='schema')), name="redoc"),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
