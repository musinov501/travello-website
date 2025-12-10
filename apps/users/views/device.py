from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apps.users.serializers.device_serializer import (
    DeviceRegistrationSerializer,
    DeviceListSerializer,
    DeviceUpdateSerializer
)
from apps.users.models.device import Device


class RegisterDeviceView(CreateAPIView):
    
    serializer_class = DeviceRegistrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_client_ip(self):
       
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = self.request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
    
    def create(self, request, *args, **kwargs):
      
        data = request.data.copy()
        
      
        if 'ip_address' not in data:
            data['ip_address'] = self.get_client_ip()
        
        serializer = self.get_serializer(data=data)
        
        try:
            serializer.is_valid(raise_exception=True)
            device = serializer.save()
            
            response_data = {
                "message": "Device registered successfully",
                "device": {
                    "id": device.id,
                    "device_token": str(device.device_token),
                    "device_id": device.device_id,
                    "device_type": device.device_type,
                    "device_model": device.device_model,
                    "is_active": device.is_active,
                    "registered_at": device.first_login,
                    "last_login": device.last_login,
                }
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except serializers.ValidationError as e:
         
            if 'device_id' in e.detail:
                error_detail = e.detail['device_id']
                
               
                if isinstance(error_detail, str) and 'already registered' in error_detail.lower():
                    updated_device = getattr(serializer, '_updated_device', None)
                    
                    if updated_device:
                        return Response({
                            "message": "Device information updated successfully",
                            "device": {
                                "id": updated_device.id,
                                "device_token": str(updated_device.device_token),
                                "device_id": updated_device.device_id,
                                "device_type": updated_device.device_type,
                                "device_model": updated_device.device_model,
                                "is_active": updated_device.is_active,
                                "last_login": updated_device.last_login,
                            }
                        }, status=status.HTTP_200_OK)
            
           
            raise


class DeviceListView(ListAPIView):
    """
    List all devices for the authenticated user.
    """
    serializer_class = DeviceListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Device.objects.filter(
            user=self.request.user
        ).select_related('app_version').order_by('-last_login')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
       
        active_count = queryset.filter(is_active=True, logged_out_at__isnull=True).count()
        total_count = queryset.count()
        
        response_data = {
            "count": total_count,
            "active_devices": active_count,
            "inactive_devices": total_count - active_count,
            "devices": serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class DeviceDetailView(RetrieveUpdateAPIView):
    """
    Retrieve or update a specific device.
    """
    serializer_class = DeviceListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DeviceUpdateSerializer
        return DeviceListSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
      
        output_serializer = DeviceListSerializer(instance)
        
        return Response({
            "message": "Device updated successfully",
            "device": output_serializer.data
        })


class DeviceLogoutView(DestroyAPIView):
    """
    Logout from a specific device (mark as inactive).
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Device.objects.filter(user=self.request.user, is_active=True)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.logout()
        
        return Response({
            "message": "Device logged out successfully",
            "device_id": instance.id
        }, status=status.HTTP_200_OK)