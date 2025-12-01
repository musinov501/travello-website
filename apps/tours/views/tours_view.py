from rest_framework import generics, permissions
from apps.tours.models.tours import Tour
from apps.tours.serializers.tour_serializer import TourSerializer


class TourListView(generics.ListAPIView):
    queryset = Tour.objects.filter(status=True)
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]


class TourDetailView(generics.RetrieveAPIView):
    queryset = Tour.objects.filter(status=True)
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]

class TourCreateView(generics.CreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAdminUser]


class TourUpdateView(generics.UpdateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAdminUser]


class TourDeleteView(generics.DestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAdminUser]
