from django.urls import path
from apps.tours.views.tours_view import (
    TourListView, TourDetailView, TourCreateView,
    TourUpdateView, TourDeleteView
)

app_name = 'tours'

urlpatterns = [
    path('', TourListView.as_view(), name='list'),
    path('<int:pk>/', TourDetailView.as_view(), name='detail'),
    path('create/', TourCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TourUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TourDeleteView.as_view(), name='delete'),
]


