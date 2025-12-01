from django.urls import path
from apps.hotels.views.hotel_view import (
    HotelListView,
    HotelDetailView,
    HotelCreateView,
    HotelUpdateView,
    HotelDeleteView,
)

app_name = 'hotels'

urlpatterns = [
    path('', HotelListView.as_view(), name='hotel-list'),
    path('<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('create/', HotelCreateView.as_view(), name='hotel-create'),
    path('<int:pk>/update/', HotelUpdateView.as_view(), name='hotel-update'),
    path('<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel-delete')
]