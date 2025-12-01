from rest_framework import generics, permissions
from apps.excursions.models import Excursion
from apps.excursions.serializers.excursion_serializer import ExcursionSerializer

class ExcursionListView(generics.ListAPIView):
    queryset = Excursion.objects.filter(is_available=True)
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.AllowAny]

class ExcursionDetailView(generics.RetrieveAPIView):
    queryset = Excursion.objects.filter(is_available=True)
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.AllowAny]

class ExcursionCreateView(generics.CreateAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.IsAdminUser]

class ExcursionUpdateView(generics.UpdateAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.IsAdminUser]

class ExcursionDeleteView(generics.DestroyAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.IsAdminUser]
