from rest_framework import serializers
from apps.excursions.models.excursion import Excursion

class ExcursionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = "__all__"
        read_only_fields = ('id', 'created_at', 'updated_at')
        
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value
    
    def validate_duration_hours(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than zero.")
        return value
    
    def validate(self, data):
        if 'title' in data and 'location' in data:
            if Excursion.objects.filter(title=data['title'], location=data['location']).exists():
                raise serializers.ValidationError("An excursion with this title and location already exists.")
        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_available'] = 'Yes' if instance.is_available else 'No'
        return representation
    
    