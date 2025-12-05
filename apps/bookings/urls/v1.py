from django.urls import path
from apps.bookings.views.booking_view import BookingCreateView, BookingListView, BookingDetailView, BookingCancelView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list-all'),  # all bookings
    path('<str:booking_type>/', BookingListView.as_view(), name='booking-list-by-type'),  # filtered
    path("create/", BookingCreateView.as_view(), name="booking-create"),
    path("<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("<int:pk>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),
]
