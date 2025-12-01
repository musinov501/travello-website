from rest_framework.permissions import BasePermission
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.users.models.device import Device


class IsMobileOrWebUser(BasePermission):
  

    def has_permission(self, request, view):
      
        if request.user and request.user.is_authenticated:
            return True

        
        device_token = request.headers.get("device_token")
        if not device_token:
            raise CustomException(message_key="TOKEN_IS_NOT_PROVIDED")

        try:
            device = Device.objects.get(device_token=device_token)
        except Device.DoesNotExist:
            raise CustomException(message_key="NOT_FOUND")
        

        
        request.device = device
        return True
