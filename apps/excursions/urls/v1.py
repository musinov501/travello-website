from django.urls import path
from apps.excursions.views.excursion_views import (
    ExcursionListView,
    ExcursionDetailView,
    ExcursionCreateView,
    ExcursionUpdateView,
    ExcursionDeleteView
)

app_name = 'excursions'

urlpatterns = [
    path('', ExcursionListView.as_view(), name='excursion-list'),
    path('<int:pk>/', ExcursionDetailView.as_view(), name='excursion-detail'),
    path('create/', ExcursionCreateView.as_view(), name='excursion-create'),
    path('<int:pk>/update/', ExcursionUpdateView.as_view(), name='excursion-update'),
    path('<int:pk>/delete/', ExcursionDeleteView.as_view(), name='excursion-delete'),
]
