from django.urls import path, include


urlpatterns = [
    path('users/', include('apps.users.urls.v1')),
    path('device/', include('apps.users.urls.v1')),
    path('tours/', include('apps.tours.urls.v1')),
    path('hotels/', include('apps.hotels.urls.v1')),
    path('excursions/', include('apps.excursions.urls.v1')),
]