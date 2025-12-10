from rest_framework import generics, permissions
from apps.excursions.models import Excursion
from apps.excursions.serializers.excursion_serializer import ExcursionSerializer
from apps.shared.utils.custom_response import CustomResponse


class ExcursionListView(generics.ListAPIView):
    queryset = Excursion.objects.filter(is_available=True)
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return CustomResponse.success(
            request=request,
            data=serializer.data
        )


class ExcursionDetailView(generics.RetrieveAPIView):
    queryset = Excursion.objects.filter(is_available=True)
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        try:
            excursion = self.get_object()
        except Exception:
            return CustomResponse.not_found(request=request)

        serializer = self.get_serializer(excursion)
        return CustomResponse.success(
            request=request,
            data=serializer.data
        )


class ExcursionCreateView(generics.CreateAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return CustomResponse.validation_error(
                request=request,
                errors=serializer.errors
            )

        excursion = serializer.save()

        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=ExcursionSerializer(excursion).data
        )


class ExcursionUpdateView(generics.UpdateAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
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
            data=serializer.data
        )


class ExcursionDeleteView(generics.DestroyAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
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


