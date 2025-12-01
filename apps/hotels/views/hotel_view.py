
from rest_framework import generics, permissions
from apps.hotels.models import Hotel
from apps.hotels.serializers.hotel_serializer import HotelSerializer, HotelListSerializer


class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.filter(is_available=True)
    serializer_class = HotelListSerializer
    permission_classes = [permissions.AllowAny]



class HotelDetailView(generics.RetrieveAPIView):
    queryset = Hotel.objects.filter(is_available=True)
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]



class HotelCreateView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]



class HotelUpdateView(generics.UpdateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]


class HotelDeleteView(generics.DestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]
