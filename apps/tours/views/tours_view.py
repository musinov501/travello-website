from rest_framework import generics, permissions
from apps.tours.models.tours import Tour
from apps.tours.serializers.tour_serializer import TourSerializer
from apps.shared.utils.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser


class TourListView(generics.ListAPIView):
    queryset = Tour.objects.filter(status=True)
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class TourDetailView(generics.RetrieveAPIView):
    queryset = Tour.objects.filter(status=True)
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        try:
            tour = self.get_object()
        except Exception:
            return CustomResponse.not_found(request=request)

        serializer = self.get_serializer(tour)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class TourCreateView(generics.CreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return CustomResponse.validation_error(
                request=request,
                errors=serializer.errors
            )

        tour = serializer.save()

        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=TourSerializer(tour).data
        )


class TourUpdateView(generics.UpdateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return CustomResponse.not_found(request=request)

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return CustomResponse.validation_error(
                request=request,
                errors=serializer.errors
            )

        serializer.save()

        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=serializer.data
        )


class TourDeleteView(generics.DestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
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
