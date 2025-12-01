from rest_framework import serializers
from apps.tours.models.tours import Tour

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


