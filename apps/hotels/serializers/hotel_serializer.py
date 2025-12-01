from rest_framework import serializers
from apps.hotels.models.hotels import Hotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            'id',
            'name',
            'location',
            'rating',
            'description',
            'price_per_night',
            'available_rooms',
            'is_available',
            'main_image',
            'has_wifi',
            'has_pool',
            'has_breakfast',
            'has_parking',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
        
class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "location",
            "rating",
            "price_per_night",
            "available_rooms",
            "is_available",
            "main_image",
        ]
        
        read_only_fields = fields
        
        