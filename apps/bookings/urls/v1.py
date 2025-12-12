from django.urls import path
from apps.bookings.views.booking_view import BookingCreateView, BookingListView, BookingDetailView, BookingCancelView

urlpatterns = [
    path("create/", BookingCreateView.as_view(), name="booking-create"),
    path("<int:pk>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),
    path("<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path('<str:booking_type>/', BookingListView.as_view(), name='booking-list-by-type'),
    path('', BookingListView.as_view(), name='booking-list-all'),  
]


