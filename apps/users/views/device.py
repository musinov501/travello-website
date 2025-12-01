from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView
from apps.users.serializers.device_serializer import DeviceResgitrationSerializer, DeviceListSerializer
from apps.users.models.device import Device


class RegisterDeviceView(CreateAPIView):
    serializer_class = DeviceResgitrationSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    
class DeviceListView(ListAPIView):
    serializer_class = DeviceListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)
