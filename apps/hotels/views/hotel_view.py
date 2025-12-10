
from rest_framework import generics, permissions
from apps.hotels.models import Hotel
from apps.hotels.serializers.hotel_serializer import HotelSerializer, HotelListSerializer
from apps.shared.utils.custom_response import CustomResponse


class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.filter(is_available=True)
    serializer_class = HotelListSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request,  *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return CustomResponse.success(
            request=request,
            data=serializer.data
        )    



class HotelDetailView(generics.RetrieveAPIView):
    queryset = Hotel.objects.filter(is_available=True)
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        try:
            hotel = self.get_object()
        except Exception:
            return CustomResponse.not_found(request=request)
        
        serializer = self.get_serializer(hotel)
        return CustomResponse.success(
            request=request,
            data=serializer.data
        )



class HotelCreateView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                request=request,
                errors = serializer.errors
            )
        hotel =  serializer.save()
        
        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=HotelSerializer(hotel).data
        )
        



class HotelUpdateView(generics.UpdateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]
    
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return CustomResponse.not_found(request=request)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                request=request,
                errors=serializer.errors
            )
        
        serializer.save()
        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=request.data
        )
    


class HotelDeleteView(generics.DestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return CustomResponse.not_found(request=request)
        
        instance.delete()
        
        return CustomResponse.success(
            message_key="DELETED",
            request=request
        )
        
