# apps/bookings/views/booking_views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.bookings.models.booking_model import Booking
from apps.bookings.serializers.booking_serializer import BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = serializer.save()
        return Response(
            {
                "success": True,
                "message": "Booking created successfully",
                "data": BookingSerializer(booking).data
            },
            status=status.HTTP_201_CREATED
        )
# views.py
class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        booking_type = self.kwargs.get('booking_type', None) 

        queryset = Booking.objects.filter(user=user).order_by('-created_at')

        if booking_type == "hotels":
            queryset = queryset.filter(hotel__isnull=False)
        elif booking_type == "tours":
            queryset = queryset.filter(tour__isnull=False)
        elif booking_type == "excursions":
            queryset = queryset.filter(excursion__isnull=False)

        return queryset


    def list(self, request, *args, **kwargs):
        bookings = self.get_queryset()
        return Response({
            "success": True,
            "count": bookings.count(),
            "data": BookingSerializer(bookings, many=True).data
        })



class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        booking = self.get_object()

        # Ensure user is owner
        if booking.user != request.user:
            return Response(
                {"success": False, "message": "Not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "success": True,
            "data": BookingSerializer(booking).data
        })


class BookingCancelView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        booking = self.get_object()

        # Ensure user is owner
        if booking.user != request.user:
            return Response(
                {"success": False, "message": "Not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status == "canceled":
            return Response(
                {"success": False, "message": "Booking already canceled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Restore rooms if hotel booking
        if booking.hotel:
            booking.hotel.available_rooms += booking.guests
            booking.hotel.save()

        booking.status = "canceled"
        booking.save()

        return Response({
            "success": True,
            "message": "Booking canceled successfully"
        })
