from apps.shared.exceptions.custom_exceptions import CustomException
from apps.users.models.device import Device
from apps.shared.models import Language

class DeviceAndLanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        device_token = request.headers.get('Device-Token') or request.headers.get('device_token')

        if device_token:
           
            request.device_type = "MOBILE"
            try:
                device = Device.objects.get(device_token=device_token)
                
                request.lang = request.headers.get("Accept-Language") or device.language or Language.UZ
            except Device.DoesNotExist:
                raise CustomException(message_key="NOT_FOUND")
        else:
           
            request.device_type = "WEB"
           
            request.lang = request.headers.get("Accept-Language", Language.UZ)

        response = self.get_response(request)
        return response
