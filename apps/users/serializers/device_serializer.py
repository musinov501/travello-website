from rest_framework import serializers
from apps.users.models.device import Device, AppVersion
from apps.shared.exceptions.custom_exceptions import CustomException


class DeviceResgitrationSerializer(serializers.ModelSerializer):
    
    app_version = serializers.CharField()
    
    
    class Meta:
        model = Device
        fields = [
            "id",
            "device_model",
            "operation_version",
            "device_type",
            "device_id",
            "ip_address",
            "app_version",
            "firebase_token",
            "language",
            "theme",
            "device_token"
            
       ]
        read_only_fields = ['id', "device_token"]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
        
    def validate_device_model(self, device_model):
        if 'script' in device_model:
            raise CustomException(message_key='NOT_CREATED')
        return device_model

    def create(self, validated_data):
        version_str = validated_data.pop('app_version')
       
        app_version_obj, _ = AppVersion.objects.get_or_create(
            version=version_str,
            defaults={'device_type': validated_data.get('device_type', 'unknown')}
        )
        validated_data['app_version'] = app_version_obj
        return super().create(validated_data)
    

from rest_framework import serializers
from apps.users.models.device import Device

   
class DeviceListSerializer(serializers.ModelSerializer):
    app_version = serializers.StringRelatedField() 

    class Meta:
        model = Device
        fields = [
            'id',
            'device_model', 'operation_version', 'device_type',
            'device_id', 'ip_address', 'app_version', 'firebase_token',
            'language', 'theme', 'created_at'
        ]
        read_only_fields = fields

