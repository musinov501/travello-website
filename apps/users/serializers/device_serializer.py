from rest_framework import serializers
from apps.users.models.device import Device, DeviceType, DeviceTheme, AppVersion
from apps.shared.models import Language
from django.utils import timezone
from django.db import models 


class DeviceRegistrationSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(
        required=True,
        max_length=255,
        help_text="Unique device identifier"
    )
    device_type = serializers.ChoiceField(
        choices=DeviceType.choices,
        required=True,
        help_text="Type of device (ANDROID or IOS)"
    )
    device_model = serializers.CharField(
        required=True,
        max_length=255,
        help_text="Device model"
    )
    operation_version = serializers.CharField(
        required=True,
        max_length=155,
        help_text="OS version"
    )
    ip_address = serializers.IPAddressField(
        required=False,
        help_text="Device IP address"
    )
    

    app_version = serializers.CharField(
        required=True,
        write_only=True,  
        help_text="App version string (e.g., '1.0.0')"
    )
    
    firebase_token = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=500,
        help_text="Firebase token for push notifications"
    )
    language = serializers.ChoiceField(
        choices=Language.choices,
        required=False,
        default=Language.CRL
    )
    theme = serializers.ChoiceField(
        choices=DeviceTheme.choices,
        required=False,
        default=DeviceTheme.LIGHT
    )
    is_push_notification = serializers.BooleanField(
        required=False,
        default=True
    )
    visit_location = serializers.JSONField(
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Device
        fields = [
            'device_id',
            'device_type',
            'device_model',
            'operation_version',
            'ip_address',
            'app_version',  
            'firebase_token',
            'language',
            'theme',
            'is_push_notification',
            'visit_location'
        ]
      
        extra_kwargs = {
            'app_version': {'write_only': True}
        }
    
    def validate_device_id(self, value):
     
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Device ID must be at least 10 characters long"
            )
        return value.strip()
    
    def validate_app_version(self, value):
       
        device_type = self.initial_data.get('device_type', DeviceType.ALL)
        
     
        app_version = AppVersion.objects.filter(
            version=value,
            is_active=True
        ).filter(
            models.Q(device_type=device_type) | models.Q(device_type=DeviceType.ALL)
        ).first()
        
        if not app_version:
         
            app_version = AppVersion.objects.create(
                version=value,
                device_type=DeviceType.ALL,
                is_active=True,
                force_update=False,
                description=f"Auto-created version {value}"
            )
            print(f"✅ Created new AppVersion: {value} (ID: {app_version.id})")
        
        
        return app_version
    
    def validate_firebase_token(self, value):
      
        if value:
            user = self.context['request'].user
            existing = Device.objects.filter(
                firebase_token=value,
                is_active=True
            ).exclude(user=user).first()
            
            if existing:
                existing.is_active = False
                existing.save(update_fields=['is_active'])
        
        return value
    
    def validate(self, data):
       
        user = self.context['request'].user
        device_id = data.get('device_id')
        
        
        existing_device = Device.objects.filter(device_id=device_id).first()
        
        if existing_device:
            if existing_device.user == user:
               
                for key, value in data.items():
                    setattr(existing_device, key, value)
                
                existing_device.is_active = True
                existing_device.logged_out_at = None
                existing_device.save()
                
                
                self._updated_device = existing_device
                
                raise serializers.ValidationError({
                    "device_id": "Device already registered. Device information updated.",
                    "updated": True,
                    "device_token": str(existing_device.device_token)
                })
            else:
                raise serializers.ValidationError({
                    "device_id": "This device is already registered to another account."
                })
        
        return data
    
    def create(self, validated_data):
        
        user = self.context['request'].user
        
       
        device = Device.objects.create(
            user=user,
            is_active=True,
            **validated_data
        )
        
        return device


class DeviceListSerializer(serializers.ModelSerializer):
    device_type_display = serializers.CharField(
        source='get_device_type_display',
        read_only=True
    )
    theme_display = serializers.CharField(
        source='get_theme_display',
        read_only=True
    )
    language_display = serializers.CharField(
        source='get_language_display',
        read_only=True
    )
    days_since_registration = serializers.SerializerMethodField()
    session_duration = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    app_version_info = serializers.SerializerMethodField()
    is_logged_in = serializers.BooleanField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Device
        fields = [
            'id',
            'device_token',
            'device_id',
            'device_type',
            'device_type_display',
            'device_model',
            'display_name',
            'operation_version',
            'ip_address',
            'is_active',
            'is_logged_in',
            'status',
            'language',
            'language_display',
            'theme',
            'theme_display',
            'is_push_notification',
            'is_auth_password',
            'first_login',
            'last_login',
            'logged_out_at',
            'days_since_registration',
            'session_duration',
            'app_version_info',
            'visit_location',
        ]
        read_only_fields = [
            'id',
            'device_token',
            'first_login',
            'last_login',
            'logged_out_at'
        ]
    
    def get_days_since_registration(self, obj):
        
        if obj.first_login:
            delta = timezone.now() - obj.first_login
            return delta.days
        return 0
    
    def get_session_duration(self, obj):
   
        duration = obj.session_duration
        
        if duration:
            days = duration.days
            hours = duration.seconds // 3600
            
            if days > 0:
                return f"{days} days, {hours} hours"
            elif hours > 0:
                return f"{hours} hours"
            else:
                minutes = duration.seconds // 60
                return f"{minutes} minutes"
        
        return "N/A"
    
    def get_status(self, obj):
       
        if not obj.is_active:
            return "logged_out"
        
        if obj.logged_out_at:
            return "logged_out"
        
        if obj.last_login:
            delta = timezone.now() - obj.last_login
            if delta.days > 30:
                return "stale"
            elif delta.days > 7:
                return "idle"
        
        return "active"
    
    def get_app_version_info(self, obj):
      
        if obj.app_version:
            return {
                "id": obj.app_version.id,
                "version": obj.app_version.version,
                "force_update": obj.app_version.force_update,
                "is_latest": obj.app_version.is_active,
                "description": obj.app_version.description
            }
        return None


class DeviceUpdateSerializer(serializers.ModelSerializer):
  
    
    language = serializers.ChoiceField(
        choices=Language.choices,
        required=False
    )
    theme = serializers.ChoiceField(
        choices=DeviceTheme.choices,
        required=False
    )
    
    class Meta:
        model = Device
        fields = [
            'language',
            'theme',
            'is_push_notification',
            'is_auth_password',
            'firebase_token',
            'visit_location'
        ]
    
    def validate_firebase_token(self, value):
       
        if value:
            existing = Device.objects.filter(
                firebase_token=value,
                is_active=True
            ).exclude(id=self.instance.id).first()
            
            if existing:
                raise serializers.ValidationError(
                    "This Firebase token is already registered to another device."
                )
        
        return value
    
    def update(self, instance, validated_data):
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance